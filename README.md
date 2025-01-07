## SurfsUp: SQLAlchemy & Flask Climate Analysis

This repository contains a climate analysis project focused on historical weather data from Hawaii. Using an SQLite database and SQLAlchemy ORM, the goal is to explore precipitation and temperature trends, then serve these findings via a Flask API.

> **Note:** ChatGPT was used to format this README and troubleshoot code.


### Key Features
SQLAlchemy & ORM

Automated reflection of database tables (measurement and station).
Simple queries for retrieving precipitation, station, and temperature data.
Jupyter Notebook Analysis

Exploratory data analysis on precipitation trends for the last 12 months.
Identification of the most active weather station and histogram of temperature observations.
Flask API

Retrieves data from queries in JSON format.
Users can specify date ranges to get min, max, and average temperature data.
