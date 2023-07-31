from flask import Flask, render_template, request, send_file
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mapclassify
import io
import psycopg2
import pandas as pd
from decimal import Decimal

app = Flask(__name__)
conn = psycopg2.connect(
    database="bike",
    user="postgres",
    password="<new_password>",
    host="localhost",
    port="5432",
)
# Cursor erstellen
cursor = conn.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/filter", methods=["POST"])
def filter_data():
    start_datum = request.form.get("start_datum")
    end_datum = request.form.get("end_datum")
    delikt = request.form.get("delikt")
    schadenshoehe_min = request.form.get("schadenshoehe_min")

    # SQL-Abfrage für FILTERN nach bestimmtem Zeitraum
    query1 = """
        SELECT *
        FROM fahrraddiebstahl_edited
        WHERE angelegt_am BETWEEN %s AND %s
    """
    cursor.execute(query1, (start_datum, end_datum))
    data1 = cursor.fetchall()

    # SQL-Abfrage für FILTERN nach bestimmtem Delikt
    query2 = """
        SELECT *
        FROM fahrraddiebstahl_edited
        WHERE delikt = %s
    """
    cursor.execute(query2, (delikt,))
    data2 = cursor.fetchall()

    # SQL-Abfrage für FILTERN nach bestimmter schadenshoehe
    query3 = """
        SELECT *
        FROM fahrraddiebstahl_edited
        WHERE schadenshoehe > %s
    """
    cursor.execute(query3, (schadenshoehe_min,))
    data3 = cursor.fetchall()

    return render_template("index.html", data1=data1, data2=data2, data3=data3)


def generate_geo_plot():
    cursor = conn.cursor()

    # SQL query to fetch data from the database
    query = """
        SELECT LOR, ANGELEGT_AM, DELIKT, SCHADENSHOEHE
        FROM fahrraddiebstahl_edited
    """
    cursor.execute(query)

    # Fetch all rows as a list of tuples
    data = cursor.fetchall()

    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data, columns=["LOR", "ANGELEGT_AM", "DELIKT", "SCHADENSHOEHE"])

    df["SCHADENSHOEHE"] = df["SCHADENSHOEHE"].apply(
        lambda x: float(x) if isinstance(x, Decimal) else x
    )

    # .geojson-datei einlesen
    geojson_data = gpd.read_file("/home/krinux/dbs/lor_planungsraeume_2021.geojson")

    # convert 'PLR_ID' in der .geojson-Datei als integer, um mit der 'LOR'-Spalte in der CSV-datei uebereinzustimmen
    geojson_data["PLR_ID"] = geojson_data["PLR_ID"].astype(int)

    # Merge beide Dateien basierend auf PLR_ID ^ LOR
    merged_data = geojson_data.merge(df, left_on="PLR_ID", right_on="LOR")

    # 1 Attribut zum visualisieren auswaehlen
    column_to_map = "SCHADENSHOEHE"

    # Plot einrichten
    fig, ax = plt.subplots()
    merged_data.plot(column=column_to_map, cmap="coolwarm", legend=False, ax=ax)

    # Legende erstellen
    values = merged_data[column_to_map]
    classifier = mapclassify.Quantiles(
        values, k=5
    )  # 'k' hier: gewÃ¼nschte Anzahl von Klassen
    colors = plt.cm.coolwarm(classifier(values))
    handles = []
    for i, (class_min, class_max) in enumerate(
        zip(classifier.bins[:-1], classifier.bins[1:])
    ):
        color = colors[i]
        patch = mpatches.Patch(color=color, label=f"{class_min:.2f} - {class_max:.2f}")
        handles.append(patch)

    # insert legende
    ax.legend(handles=handles, loc="lower right")

    # Titel fuer den Plot
    ax.set_title("Fahrraddiebstahl in Berlin - Schadenshoehe")

    # Sp. den plot image zu einem BytesIO objekt
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype="image/png")


def generate_histogram():
    cursor = conn.cursor()

    # SQL query to fetch data from the database
    query = """
        SELECT tatzeit_anfang
        FROM fahrraddiebstahl_edited
    """
    cursor.execute(query)

    # Fetch all rows as a list of tuples
    data = cursor.fetchall()

    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data, columns=["tatzeit_anfang"])

    # Extract the hour from the timestamp column
    df["hour"] = df["tatzeit_anfang"].dt.hour

    # Plot the histogram
    plt.figure()
    plt.hist(df["hour"], bins=24, edgecolor="black")
    plt.xlabel("Uhrzeit")
    plt.ylabel("Frequenz")
    plt.title("Diebstähle per Uhrzeit")

    # Save the plot image to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype="image/png")


def generate_beautiful_plot():
    # SQL query to fetch data from the database
    query = """
        SELECT f.LOR, f.ANGELEGT_AM, f.DELIKT, f.SCHADENSHOEHE, l.PLR_ID, b.BEZ, b.Gemeinde_schluessel
        FROM fahrraddiebstahl_edited f
        LEFT JOIN lor_planungsraeume_2021 l ON f.LOR = l.PLR_ID
        LEFT JOIN bezirksgrenzen b ON f.BEZ = b.Gemeinde_schluessel
    """

    # Fetch data from the database
    cursor.execute(query)
    data = cursor.fetchall()

    # Convert data to pandas DataFrame
    columns = [
        "LOR",
        "ANGELEGT_AM",
        "DELIKT",
        "SCHADENSHOEHE",
        "PLR_ID",
        "BEZ",
        "Gemeinde_schluessel",
    ]
    df = pd.DataFrame(data, columns=columns)

    print(df["f_pk"].unique())

    # Diebstähle zählen
    diebstahl_pro_bezirk = (
        df.groupby("Gemeinde_schluessel").size().reset_index(name="Anzahl_Diebstähle")
    )

    # Merge der Diebstahldaten mit den Bezirksgrenzen
    merged = pd.merge(
        df,
        diebstahl_pro_bezirk,
        left_on="Gemeinde_schluessel",
        right_on="Gemeinde_schluessel",
        how="left",
    )

    # Visualisierung
    fig, ax = plt.subplots(figsize=(12, 8))
    merged.plot(
        column="Anzahl_Diebstähle",
        cmap="Blues",
        linewidth=0.8,
        ax=ax,
        edgecolor="0.8",
        legend=True,
    )

    # Save the plot image to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype="image/png")


@app.route("/beautifulplot")
def beautifulplot():
    return generate_beautiful_plot()


@app.route("/plot")
def plot():
    return generate_geo_plot()


@app.route("/histogram")
def histogram():
    return generate_histogram()


if __name__ == "__main__":
    app.run(debug=True)
