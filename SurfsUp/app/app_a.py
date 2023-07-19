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
        f'/api/v1.0/(start date)<br/>'
        f'/api/v1.0/(start date)/(end date)'
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
    # query station and station names
    station_names = session.query(Station.station, Station.name).all()
    
    session.close()

    station_list = {}

    for station, name in station_names:
        # initiate dictionary
        station_dict = {}
        # #setup station and station name as key value pairs for dict
        station_dict[station] = name 
        #append dict into list
        station_list.update(station_dict) 

    return jsonify(station_list)


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
def temp_min_max_avg(start):
    session = Session(engine)
    tdata = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
   func.max(Measurement.tobs)).\
    filter(Measurement.date >=  start).\
    order_by(Measurement.date).all()
    templist = []
    for TMIN, TAVG, TMAX in stats:
        stats_dict = {}
        stats_dict['TMIN'] = tdata[0]
        stats_dict['TAVG'] = tdata[1]
        stats_dict['TMAX'] = tdata[2]
        templist.append(stats_dict)

    session.close()

    return jsonify(templist)

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX 
# for the dates from the start date to the end date, inclusive.

#@app.route("/api/v1.0/<start>", defaults = {'end': None})
@app.route("/api/v1.0/<start>/<end>")
def temps_min_max_avg(start,end):
    session = Session(engine)
    # specified end and start dates
    if end != None:
        tdata = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
   func.max(Measurement.tobs)).filter(Measurement.date >=start).\
    filter(Measurement.date<= end).all()
    # no specified end date
    else:
        tdata = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    tdatalist = []
    for TMIN, TAVG, TMAX in tdata:
        stats_dict = {}
        #tdatalist.append(TMIN)
        #tdatalist.append(TAVG)
        #tdatalist.append(TMAX)
        stats_dict["Min_temp"] = tdata[0][0]
        stats_dict["Avg_temp"] = tdata[0][1]
        stats_dict["Max_temp"] = tdata[0][2]
        tdatalist.append(stats_dict)

    return jsonify(tdatalist)


if __name__ == '__main__':
    app.run(debug=True)
