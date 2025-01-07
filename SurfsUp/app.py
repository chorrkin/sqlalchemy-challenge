# app.py

# -----------------------------
# Imports
# -----------------------------
import datetime as dt

import numpy as np
import pandas as pd

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# -----------------------------
# Database Setup
# -----------------------------
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# -----------------------------
# Flask Setup
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Flask Routes
# -----------------------------
@app.route("/")
def home():
    """
    Homepage that lists all available routes.
    Includes simple inline CSS for styling.
    """
    return (
        f"<style>"
        f"body {{"
        f"    font-family: Arial, sans-serif;"
        f"    margin: 20px;"
        f"    background-color: #f0f8ff;"  
        f"}}"
        f"h2 {{"
        f"    color: red;"
        f"    text-align: center;"
        f"}}"
        f"</style>"
        f"<center><h2><font color='red'>Holiday vacation in Honolulu, Hawaii climate analysis homepage.</font></h2></center>"
        f"<h3>List of available routes</h3>"
        f"<ul>"
        f"<li><a href='/api/v1.0/precipitation' target='_blank'>/api/v1.0/precipitation</a></li>"
        f"<li><a href='/api/v1.0/stations' target='_blank'>/api/v1.0/stations</a></li>"
        f"<li><a href='/api/v1.0/tobs' target='_blank'>/api/v1.0/tobs</a></li>"
        f"<li>/api/v1.0/&lt;startdate&gt; <i>(use mmddyyyy)</i></li>"
        f"<li>/api/v1.0/&lt;startdate&gt;/&lt;enddate&gt; <i>(use mmddyyyy/mmddyyyy)</i></li>"
        f"</ul>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """
    Returns a JSON dictionary of date: precipitation for the last 12 months of data.
    """
    past_one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    with Session(engine) as session:
        # Query date and precipitation scores
        one_year_data = (
            session.query(Measurement.date, Measurement.prcp)
            .filter(Measurement.date >= past_one_year)
            .all()
        )

    # Create a dictionary with date as the key and prcp as the value
    precip_dict = {date: prcp for date, prcp in one_year_data}
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def station_list():
    """
    Returns a JSON list of all weather stations.
    """
    with Session(engine) as session:
        results = session.query(Station.station).all()

    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temps():
    """
    Returns a JSON dictionary of date: temperature observations
    for the most active station from the past year of data.
    """
    past_one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    with Session(engine) as session:
        most_active = (
            session.query(Measurement.date, Measurement.tobs)
            .filter(Measurement.station == 'USC00519281')
            .filter(Measurement.date >= past_one_year)
            .all()
        )

    temps_dict = {date: tobs for date, tobs in most_active}
    return jsonify(temps_dict)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_stats(start=None, end=None):
    """
    Returns a JSON list of [min_temp, max_temp, avg_temp] 
    for the given start date, or start to end date range.
    
    Date format expected: mmddyyyy
    """
    # Try to convert the start date string to a datetime object
    try:
        start_date = dt.datetime.strptime(start, "%m%d%Y")
    except ValueError:
        return jsonify({"error": f"Invalid start date format: {start}. Use mmddyyyy."}), 400

    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    # If no end date is provided, query from the start date to the end of data
    if not end:
        with Session(engine) as session:
            results = (
                session.query(*selection)
                .filter(Measurement.date >= start_date)
                .all()
            )
        temp_list = list(np.ravel(results))
        return jsonify(temp_list)
    else:
        # Convert the end date string to a datetime object
        try:
            end_date = dt.datetime.strptime(end, "%m%d%Y")
        except ValueError:
            return jsonify({"error": f"Invalid end date format: {end}. Use mmddyyyy."}), 400

        with Session(engine) as session:
            results = (
                session.query(*selection)
                .filter(Measurement.date >= start_date)
                .filter(Measurement.date <= end_date)
                .all()
            )
        temp_list = list(np.ravel(results))
        return jsonify(temp_list)

# -----------------------------
# Main Check
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
