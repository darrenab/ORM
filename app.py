import datetime as dt
import numpy as np
import pandas as pd 

import sqlalchemy   
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func  

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

Base=automap_base()

Base.prepare(engine,reflect=True)

#save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session=Session(engine)


app=Flask(__name__)

@app.route("/")
def home():
    return (
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )

# precipitation data
@app.route('/api/v1.0/precipitation')
def rainfall():
    response=session.query(Measurement).all()

    rainDates =[]
    for day in response:
        prcpDict ={}
        prcpDict['date']=day.date
        prcpDict['precipitation']=day.prcp
        
        rainDates.append(prcpDict)
    raindays=list(np.ravel(rainDates))
    return jsonify(raindays) 

#station names
@app.route('/api/v1.0/stations') 
def staionNames():
    response=session.query(Station.station).all()
    names=list(np.ravel(response))

    return jsonify(names)

#temp for the last 12 months
@app.route('/api/v1.0/tobs')
def temperature():
    temp=session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date>='2016-08-23').all()
    last12temp=list(np.ravel(temp))
    return jsonify (last12temp)

#min,max,avg's
@app.route('/api/v1.0/start')
def onOrAfter():
    metrics=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= '2017-05-01').all()
    startingMay=list(np.ravel(metrics))
    return jsonify (startingMay)

@app.route('/api/v1.0/start/end')
def within():
    metrics2=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= '2016-05-01').filter(Measurement.date <= '2016-05-31').all()
    justMay=list(np.ravel(metrics2))
    return jsonify (justMay)





if __name__ == '__main__':
    app.run(debug=True)