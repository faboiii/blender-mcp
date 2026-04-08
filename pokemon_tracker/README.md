# Pokemon Karten Tracker

Eine Web-Anwendung zum **Erfassen**, **Auswerten** und **Vergleichen** von Pokemon Sammelkarten.

## Features

| Feature | Beschreibung |
|---|---|
| **Karten suchen** | Suche via [Pokemon TCG API](https://pokemontcg.io) nach Name |
| **Sammlung verwalten** | Karten hinzufügen, bearbeiten, löschen, Anzahl pflegen |
| **Bewertung** | Marktpreise (Niedrig/Mittel/Hoch), zustandsbasierter Schätzwert |
| **Zustände** | M · NM · LP · MP · HP · D (mit Wertmultiplikator) |
| **Grading** | PSA / BGS / CGC-Grade erfassen (automatischer Wertbonus) |
| **Vergleich** | Bis zu 4 Karten nebeneinander vergleichen |
| **Statistiken** | Diagramme für Seltenheit & Element, Top-10-Liste, G/V-Rechnung |
| **Filter & Sort** | Sammlung nach Name, Zustand und Wert filtern/sortieren |

## Schnellstart

```bash
cd pokemon_tracker
pip install -r requirements.txt
python app.py
```

Dann im Browser öffnen: **http://localhost:8000**

## Zustandsskala

| Kürzel | Bezeichnung | Wertfaktor |
|---|---|---|
| M  | Mint – perfekter Zustand | ×1.20 |
| NM | Near Mint – fast perfekt | ×1.00 |
| LP | Lightly Played – leicht bespielt | ×0.85 |
| MP | Moderately Played – mäßig bespielt | ×0.65 |
| HP | Heavily Played – stark bespielt | ×0.45 |
| D  | Damaged – beschädigt | ×0.25 |

## Grading-Bonus

| PSA-Grade | Wertmultiplikator |
|---|---|
| 10 | ×3.0 |
| 9  | ×2.0 |
| 8  | ×1.5 |

## Projektstruktur

```
pokemon_tracker/
├── app.py            – FastAPI Hauptanwendung (Routen, Logik)
├── database.py       – SQLAlchemy Modelle + SQLite Setup
├── schemas.py        – Pydantic Schemas
├── pokemon_api.py    – Pokemon TCG API Client
├── requirements.txt
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    ├── base.html
    ├── index.html        – Sammlungsübersicht
    ├── search.html       – Kartensuche
    ├── card_form.html    – Karte hinzufügen / bearbeiten
    ├── card_detail.html  – Kartendetails & Bewertung
    ├── compare.html      – Kartenvergleich
    └── statistics.html   – Statistiken & Charts
```
