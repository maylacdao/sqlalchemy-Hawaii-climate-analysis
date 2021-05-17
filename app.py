# python modules
import datetime as dt
import numpy as np
import pandas as pd

# sql modules
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# flask modules
from flask import Flask, jsonify

# set up SQLAlchemy
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# print(Base.classes.keys())

Measurement = Base.classes.measurement
Station = Base.classes.station

# session
session = Session(engine)

# Flask app
app = Flask(__name__)


@app.route("/")
def main():
    return """<html>
        <style>
            body {
                background-image: url(https://images.pexels.com/photos/2521620/pexels-photo-2521620.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940);
            }
    
            h1 {
                text-align: center;
                font-size: 70px;
                padding-top: 20px;
            }

            h2{
                text-align: left;
                font-size: 40px;
                padding-left: 20px;
            }

            ul{
                display: inline;
                
            }

            li {
                font-size: 23px;
                list-style: disc;
                padding-left: 30px;
                line-height: 1.5;
                font-weight: bold; 
            }
        </style>

    <body>
        <h1>Surf's Up: Hawaii Climate</h1>
        <h2>Available Routes</h2>
        <ul>
            <li>
                Precipitation:  /api/v1.0/precipitation      
            </li>
            <li>
                Station: /api/v1.0/stations
            </li>
            <li>
                Temperature: /api/v1.0/tobs
            </li>
            <li>
                  Start Date: /api/v1.0/<start>
            </li>
            <li>
                Start & End Dates: /api/v1.0/<start>/<end>
            </li>
        </ul>
    </body>
    </html>"""


@ app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date.desc()).all()
    session.close()
    prcp_data_list = dict(prcp_data)
    return jsonify(prcp_data_list)


@ app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(Station.station, Station.name).all()
    session.close()
    stations_list = list(all_stations)
    return jsonify(stations_list)


@ app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= year_ago).all()
    session.close()
    tobs_list = list(np.ravel(tobs_query))
    return jsonify(tobs_list)


@ app.route("/api/v1.0/<start>")
def oneDate(start):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    temp_info = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()
    temp_data = list(np.ravel(temp_info))
    return jsonify(temp_data)


@ app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    if end != "":
        temp_info = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(
                Measurement.date <= end_date).all()
        session.close()
        temp_data = list(np.ravel(temp_info))
        return jsonify(temp_data)

    else:
        temp_info = session.query(func.min(Measurement.tobs), func.avg(
            Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > end_date).all()
        session.close()
        temp_data = list(np.ravel(temp_info))
        return jsonify(temp_data)


if __name__ == "__main__":
    app.run(debug=True)
