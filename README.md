# EinsatzRaum – öffentliche Datenpakete

Dieses Repository dient als kostenfreie, öffentliche Updatequelle für die App **EinsatzRaum**.

## Zulässige Inhalte

- frei zugängliche Verwaltungs- und Gebietsdaten
- öffentliche Funktionskontakte
- Quellen- und Lizenznachweise
- fachlich geprüfte Regel- und Referenzdaten, soweit eine Weitergabe zulässig ist
- fiktive Demonstrationsdaten

## Nicht zulässige Inhalte

- private Telefonnummern oder personenbezogene Einsatzdaten
- Zugangscodes, Schlüsselstellen oder interne Objektpläne
- genaue nicht öffentliche KRITIS-Informationen
- reale Einsatzdaten
- Daten von Betroffenen, Patientinnen und Patienten oder Bewohnerinnen und Bewohnern
- ungeklärte Kopien geschützter Stoff- oder Fachdatenbanken

## Struktur

```text
manifest.json
packages/
  northeim/
    municipalities-0.1.0.json
SOURCES.md
tools/validate.py
```

`manifest.json` ist die kleine Datei, die die App beim Start abfragt. Paketdateien werden erst in einem späteren App-Inkrement heruntergeladen, per SHA-256 geprüft und anschließend atomar aktiviert.

## Aktueller Datenstand

Der Prototyp enthält zunächst nur:

- die Namen der elf Städte und Gemeinden im Landkreis Northeim
- den allgemeinen, öffentlich veröffentlichten Kontakt der Kreisverwaltung
- Quellen-, Prüf- und Sicherheitshinweise

Noch nicht enthalten sind Einwohnerzahlen, kommunale Einzelkontakte, Netzbetreiber, Einsatzkontakte, Karten, Gefahrgutdaten und Objektinformationen.

## Prüfung

GitHub Actions führt bei Änderungen `tools/validate.py` aus. Die Prüfung kontrolliert unter anderem:

- gültiges JSON
- eindeutige Paket-IDs
- vorhandene Paketdateien
- Dateigröße und SHA-256-Prüfsumme
- einige ausdrücklich verbotene, sensibel wirkende Feldnamen

Diese technische Prüfung ersetzt keine fachliche, rechtliche oder datenschutzrechtliche Freigabe.
