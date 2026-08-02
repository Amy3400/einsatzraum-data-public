# Paketformat v1

## Manifest

Die App liest `manifest.json` und vergleicht die dort angegebenen Paketversionen mit ihrer lokalen Datenbank.

Pflichtfelder eines Paketeintrags:

- `id`
- `title`
- `version`
- `type`
- `url`
- `sha256`
- `sizeBytes`
- `required`

Zusätzliche Schutzfelder:

- `sensitivity`
- `reviewStatus`
- zukünftig `appMinVersion`, `validFrom` und `validUntil`

## Aktivierungsregel

Ein zukünftiger Downloader darf ein Paket nur aktivieren, wenn:

1. der Download vollständig beendet wurde,
2. die Dateigröße stimmt,
3. SHA-256 stimmt,
4. das JSON dem erwarteten Schema entspricht,
5. die App-Version kompatibel ist,
6. kein höher eingestuftes lokales Paket unkontrolliert überschrieben wird.

Bis zur vollständigen Prüfung bleibt die vorherige Paketversion aktiv.
