# Eclipse MCP Server

Dieses Repository enthält einen einfachen MCP Server, der als Vermittler zwischen
einer Eclipse IDE und einem lokalen KI-Modell fungiert. Ziel ist es, über einen Chat-Client
Befehle an ein laufendes Eclipse-Projekt zu senden und den Quellcode mit einem lokalen
Ollama-Modell (z.B. `devstral:24b`) zu verarbeiten.

## Features

- HTTP-Endpunkte für das Erstellen und Anpassen von Dateien oder Java-Klassen
- Bereitstellen des gesamten Projekt-Quellcodes als Kontext
- Anbindung an ein lokales Ollama-Modell für KI-generierte Antworten
- Läuft auf Windows und kann von beliebigen Chat-Clients per HTTP angesprochen werden

## Voraussetzung

- Python 3.10 oder neuer
- Installation der benötigten Bibliotheken. Unter Windows kann dies z.B.
  so aussehen:
```cmd
py -m pip install flask requests
```
- Ollama muss lokal laufen, Standardport `11434`.

## Starten des Servers

```cmd
py server.py
```

Der Server lauscht auf Port `8080` und stellt u.a. folgende Endpunkte bereit:

- `POST /create-file` – legt eine neue Datei an.
- `POST /modify-java-class` – fügt Patch-Code an eine bestehende Java-Klasse an.
- `GET /project-context` – liefert den kompletten Quellcode eines Projekts.
- `POST /generate` – sendet eine Anfrage an das Ollama-Modell.

Dies ist nur ein minimaler Prototyp und muss für den produktiven Einsatz um
Eclipse-spezifische Logik, Sicherheitsaspekte und weitergehende Funktionen erweitert
werden.
