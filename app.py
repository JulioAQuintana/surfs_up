# We need to create a new Python file and import our dependencies to our code environment
import datetime as dt
import flask
import numpy as np
import pandas as pd
# Add the SQLAlchemy dependencies after the other dependencies 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Add the code to import the dependencies that we need for Flask. You'll import these right after your SQLAlchemy dependencies
from flask import Flask, jsonify
# set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")
#Now let's reflect the database into our classes
Base = automap_base()
#eflect the database:
Base.prepare(engine, reflect=True)

#create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from Python to our database
session = Session(engine)


##############################################
######### Set Up Flask #######################
##############################################
####create a Flask application called "app."
app = Flask(__name__)
#Adding 
import app

print("example __name__ = %s", __name__)

if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")
#efine the welcome route using the code below
@app.route('/')
#reate a function welcome() with a return statement
def welcome():
    return(
 # We'll use f-strings to display them for our investors
     '''Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/2017-06-01/2017-06-30''')

# def hello_world():
#     return 'Hello world'
# if __name__ ==  '__main__':
#     app.run(debug=True)
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

@app.route("/api/v1.0/stations")

#Next, we will convert our unraveled results into a list. To convert the results to a list,
# we will need to use the list function, which is list(), and then convert that array into a list.
# Then we'll jsonify the list and return it as JSON. Let's add that functionality to our code:
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#For this route, the goal is to return the temperature observations for the previous year. As with the previous routes, begin by defining the route with this code:

@app.route("/api/v1.0/tobs")
#calculate the date one year ago from the last date in the database.
#query the primary station for all the temperature observations from the previous year.
#unravel the results into a one-dimensional array and convert that array into a list
#we want to jsonify our temps list, and then return it.
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
#Add the following code to create the routes

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#create a function called stats() to put our code in
#We need to add parameters to our stats()function: a start parameter and an end parameter. For now, set them both to None.
#With the function declared, we can now create a query to select the minimum, average, and maximum temperatures from our SQLite database.
##We'll need to query our database using the list that we just made. Then, we'll unravel the results into a one-dimensional array and convert them to a list.
# Finally, we will jsonify our results and return them.
#Now we need to calculate the temperature minimum, average, and maximum with the start and end date

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

    