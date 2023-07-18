# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()
#print(Base.classes.keys())
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    #List all available API routes
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start> <br/>'
        f'/api/v1.0/<start>/<end>'
    )

#Precipitation Analysis
@app.route("/api/v1.0/precipitation")
def precipitation():

    mostrecentdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    mostrecentdate
    mostrecentdate = mostrecentdate[0]
    recent_date_dt = dt.datetime.strptime(mostrecentdate, "%Y-%m-%d").date()
    recent_date_dt
    year_ago_dt = recent_date_dt - dt.timedelta(days=365)
    year_ago_dt
    # Perform a query to retrieve the data and precipitation scores
    last_year = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago_dt).\
    order_by(Measurement.date).all()

    resultslist = []
    for date, prcp in last_year:
        results_dict = {}
        results_dict[date] = prcp
        resultslist.append(results_dict)

    return jsonify(resultslist)

#Stations
@app.route(f'/api/v1.0/stations')
def stations():
    return ''


if __name__ == '__main__':
    app.run(debug=True)