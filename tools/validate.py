from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifest.json"

FORBIDDEN_FIELD_NAMES = {
    "accessCode",
    "doorCode",
    "privateMobile",
    "patientName",
    "residentName",
    "keyLocation",
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_forbidden_fields(value: object, trail: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_trail = f"{trail}.{key}"
            if key in FORBIDDEN_FIELD_NAMES:
                findings.append(child_trail)
            findings.extend(find_forbidden_fields(child, child_trail))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_forbidden_fields(child, f"{trail}[{index}]"))
    return findings


def package_path_from_url(url: str) -> Path:
    parsed = urlparse(url)
    marker = "/main/"
    if parsed.netloc != "raw.githubusercontent.com" or marker not in parsed.path:
        raise ValueError(f"Unsupported package URL: {url}")
    relative_path = parsed.path.split(marker, maxsplit=1)[1]
    return ROOT / relative_path


def main() -> None:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH)
    if not isinstance(manifest, dict):
        raise SystemExit("manifest.json must contain an object")

    packages = manifest.get("packages")
    if not isinstance(packages, list):
        raise SystemExit("manifest.json packages must be a list")

    seen_ids: set[str] = set()
    for entry in packages:
        if not isinstance(entry, dict):
            errors.append("Manifest package entry must be an object")
            continue

        package_id = entry.get("id")
        if not isinstance(package_id, str) or not package_id:
            errors.append("Package without a valid id")
            continue
        if package_id in seen_ids:
            errors.append(f"Duplicate package id: {package_id}")
        seen_ids.add(package_id)

        try:
            package_path = package_path_from_url(str(entry.get("url", "")))
        except ValueError as error:
            errors.append(str(error))
            continue

        if not package_path.is_file():
            errors.append(f"Missing package file for {package_id}: {package_path}")
            continue

        raw = package_path.read_bytes()
        actual_sha = hashlib.sha256(raw).hexdigest()
        expected_sha = entry.get("sha256")
        if actual_sha != expected_sha:
            errors.append(
                f"SHA-256 mismatch for {package_id}: expected {expected_sha}, got {actual_sha}"
            )

        expected_size = entry.get("sizeBytes")
        if expected_size != len(raw):
            errors.append(
                f"Size mismatch for {package_id}: expected {expected_size}, got {len(raw)}"
            )

        package_json = load_json(package_path)
        forbidden = find_forbidden_fields(package_json)
        if forbidden:
            errors.append(
                f"Forbidden sensitive-looking fields in {package_id}: {', '.join(forbidden)}"
            )

    if errors:
        raise SystemExit("\n".join(f"ERROR: {error}" for error in errors))

    print(f"Validated {len(packages)} package(s).")


if __name__ == "__main__":
    main()
