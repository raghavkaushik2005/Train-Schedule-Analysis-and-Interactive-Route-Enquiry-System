from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()


def get_db_connection():

    try:

        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            connection_timeout=10
        )

        return db

    except Error as e:

        print("Database connection error:", e)

        return None


@app.route("/")
def home():

    db = get_db_connection()

    if db is None:

        return render_template(
            "results.html",
            trains=[],
            source="",
            destination="",
            error="Unable to connect to the database. Please try again."
        )

    try:

        cursor = db.cursor()

        cursor.execute("""
            SELECT DISTINCT Station_Name
            FROM train_schedule
            ORDER BY Station_Name
        """)

        stations = [row[0] for row in cursor.fetchall()]

        cursor.close()
        db.close()

        return render_template(
            "index.html",
            stations=stations
        )

    except Error as e:

        print("Database error:", e)

        if db.is_connected():
            db.close()

        return render_template(
            "results.html",
            trains=[],
            source="",
            destination="",
            error="Unable to load station information. Please try again."
        )


@app.route("/search", methods=["POST"])
def search_trains():

    source = request.form.get("source", "").strip()
    destination = request.form.get("destination", "").strip()


    if not source or not destination:

        return render_template(
            "results.html",
            trains=[],
            source=source,
            destination=destination,
            error="Please select both source and destination stations."
        )


    if source.lower() == destination.lower():

        return render_template(
            "results.html",
            trains=[],
            source=source,
            destination=destination,
            error="Source and destination stations cannot be the same."
        )


    db = get_db_connection()

    if db is None:

        return render_template(
            "results.html",
            trains=[],
            source=source,
            destination=destination,
            error="Unable to connect to the database. Please try again."
        )


    cursor = None

    try:

        cursor = db.cursor(dictionary=True)


        cursor.execute("""
            SELECT COUNT(*) AS station_count
            FROM train_schedule
            WHERE Station_Name = %s
        """, (source,))

        source_exists = cursor.fetchone()["station_count"]

        cursor.execute("""
            SELECT COUNT(*) AS station_count
            FROM train_schedule
            WHERE Station_Name = %s
        """, (destination,))

        destination_exists = cursor.fetchone()["station_count"]


        if source_exists == 0 or destination_exists == 0:

            return render_template(
                "results.html",
                trains=[],
                source=source,
                destination=destination,
                error="One or both selected stations were not found in the train schedule."
            )

        query = """
            SELECT

                s.Train_No,

                s.Station_Name AS Source_Station,

                s.Departure_Time AS Source_Departure,

                d.Station_Name AS Destination_Station,

                d.Arrival_time AS Destination_Arrival,

                CASE

                    WHEN d.Arrival_time >= s.Departure_Time

                    THEN TIMEDIFF(
                        d.Arrival_time,
                        s.Departure_Time
                    )

                    ELSE ADDTIME(
                        TIMEDIFF(
                            d.Arrival_time,
                            s.Departure_Time
                        ),
                        '24:00:00'
                    )

                END AS Journey_Duration

            FROM train_schedule s

            JOIN train_schedule d
                ON s.Train_No = d.Train_No

            WHERE s.Station_Name = %s

              AND d.Station_Name = %s

              AND s.SN < d.SN

            ORDER BY s.Train_No
        """


        cursor.execute(
            query,
            (source, destination)
        )

        trains = cursor.fetchall()


        return render_template(
            "results.html",
            trains=trains,
            source=source,
            destination=destination
        )


    except Error as e:

        print("Database error:", e)

        return render_template(
            "results.html",
            trains=[],
            source=source,
            destination=destination,
            error="A database error occurred while searching. Please try again."
        )


    finally:

        if cursor is not None:
            cursor.close()

        if db.is_connected():
            db.close()


@app.errorhandler(500)
def internal_error(error):

    return render_template(
        "results.html",
        trains=[],
        source="",
        destination="",
        error="An unexpected error occurred. Please try again."
    ), 500

if __name__ == "__main__":

    print("Starting Train Enquiry System...")

    app.run(debug=True)