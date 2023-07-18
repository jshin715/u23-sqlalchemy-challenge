# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
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
# 


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
# Create our session (link) from Python to the DB
    session = Session(engine)
    mostrecentdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    session.close()
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
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    session.close()
    stations = [row[0] for row in most_active]
    return jsonify(stations)


#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    mostrecentdate_a = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).\
    filter(Measurement.station == most_active[0][0]).all()

    session.close()
    temps = []
    for date, temp in mostrecentdate_a:
        temps_dict = {}
        temps_dict[date] = temp
        temps.append(temps_dict)
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def temp_min_max_avg():
    session = Session(engine)
    
    tdata = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), 
   func.avg(Measurement.tobs)).filter(Measurement.station == most_active[0][0]).all()
    last_year = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >=  start).\
    order_by(Measurement.date).all()

    session.close()



    return ''

@app.route("/api/v1.0/<start>/<end>")
def temp_min_max_avg_2(start,end):
    session = Session(engine)
    
    tdata = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), 
   func.avg(Measurement.tobs)).filter(Measurement.station == most_active[0][0]).all()
    last_year = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >=  start).filter(Measurement.date <  end)
    order_by(Measurement.date).all()

    session.close()



    return ''


if __name__ == '__main__':
    app.run(debug=True)