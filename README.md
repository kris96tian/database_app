# CycleWatch Berlin - (PostgreSQL-powered)

Diese App wurde entwickelt, um Daten über Fahrraddiebstähle in Berlin anzuzeigen und zu analysieren. Sie basiert auf dem Flask-Framework und verwendet PostgreSQL als Datenbank, um die Fahrraddiebstahldaten lokal zu speichern.

## Features

- **Datenfilterung**: Auf der Startseite der App können Benutzer verschiedene Filteroptionen auswählen, um die Fahrraddiebstahldaten nach Datum, Delikt oder Schadenshöhe zu filtern. Die entsprechenden Datensätze werden dann in einer tabellarischen Form angezeigt.
  
- **Interaktive Plots**:
  - Visualisierung der geografischen Verteilung der Fahrraddiebstähle in Berlin, wobei die Schadenshöhe durch eine Farbskala angezeigt wird.
  - Erstellung eines Histogramms der Diebstähle nach der Tatzeit, das die Häufigkeit von Diebstählen über einen Zeitraum von 24 Stunden darstellt.

## Technologien

Die App verwendet eine Reihe von Python-Modulen, um verschiedene Funktionen umzusetzen:

- **Flask**: Ein Webframework für Python, das verwendet wird, um die Webanwendung zu erstellen und die Routing- und Anfrageverarbeitungsfunktionen bereitzustellen.
  
- **psycopg2**: Ein Python-Adapter für PostgreSQL, der verwendet wird, um eine Verbindung zur PostgreSQL-Datenbank herzustellen und Datenbankabfragen auszuführen.
  
- **pandas**: Eine leistungsstarke Datenanalyse-Bibliothek, die verwendet wird, um die aus der Datenbank abgerufenen Daten in DataFrames zu organisieren und zu manipulieren.
  
- **geopandas**: Eine Erweiterung von Pandas, die speziell für die Verarbeitung geografischer Daten entwickelt wurde. Es wird verwendet, um geografische Daten aus einer GeoJSON-Datei einzulesen und sie mit den Fahrraddiebstahldaten zu verbinden.
  
- **matplotlib**: Eine Plotting-Bibliothek für Python, die verwendet wird, um die interaktiven Plots zu erstellen, die die geografische Verteilung der Fahrraddiebstähle und das Histogramm der Tatzeit anzeigen.
  
- **mapclassify**: Eine Bibliothek für die Klassifizierung und Visualisierung von geografischen Daten. Sie wird verwendet, um die Schadenshöhen in Klassen einzuteilen und die Farbskala für den geografischen Plot zu erstellen.

## Installation

1. Klone dieses Repository:
   ```bash
   git clone https://github.com/kris96tian/database_app.git
   cd database_app
   ```

2. Erstelle und aktiviere eine virtuelle Umgebung:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   ```

3. Installiere die erforderlichen Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

4. Stelle sicher, dass PostgreSQL installiert ist und eine Datenbank für die App existiert. Bearbeite die Konfigurationsdateien für die Verbindung zur Datenbank.

5. Starte die Flask-App:
   ```bash
   flask run
   ```

## Nutzung

- Besuche `http://127.0.0.1:5000` in deinem Browser, um die App zu verwenden.
- Wähle die gewünschten Filteroptionen aus, um die Fahrraddiebstahldaten zu durchsuchen und analysieren.
- Die App zeigt interaktive Plots, Karten und Diagramme zur Visualisierung der Daten.



<img src="https://github.com/kris96tian/database_app/blob/main/APP_screenshot_.png?raw=true" />![image](https://github.com/kris96tian/database_app/assets/92834350/78e36c72-b7d6-49e8-908b-7e3df6a0a8ac)

## Postgres from Terminal
<img src="blob:chrome-untrusted://media-app/431af720-cbaa-43d9-ace2-0136371a59f9" />![image](https://github.com/kris96tian/database_app/assets/92834350/6418d0e8-2395-481f-8e96-b95bae0ef5dc)

## Button "Plot der Diebstähle"

<img src="blob:chrome-untrusted://media-app/3978384e-c554-4688-81e4-63fdd4e1b6c5" />![image](https://github.com/kris96tian/database_app/assets/92834350/0145aa07-ecb1-4da8-8e04-b7a812e54866)
