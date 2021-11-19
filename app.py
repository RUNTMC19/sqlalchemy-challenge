import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurements = Base.classes.measurement
Stations = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")

def Welcome():
    return("""
    /Precipitation
    /Stations
    /TOBS
    /start
    /start/end
    """)

@app.route("/Precipitation")

def Precipitation():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date > query_date).order_by(Measurements.date).all()

    session.close()

    results = {date:prcp for date,prcp in results}
    return jsonify(results)

@app.route("/Stations")

def Station_Bases():
    results = session.query(Stations.station).all()

    session.close()

    return jsonify(list(np.ravel(results)))

@app.route("/TOBS")

def Temperatures ():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date > query_date).order_by(Measurements.date).all()

    session.close()

    results = {date:tobs for date,tobs in results}
    return jsonify(results)

@app.route("/Temps/<start>")
@app.route("/Temps/<start>/<end>")

def Describe (start=None,end=None):
    if not end:
        start=dt.datetime.strptime(start,"%m%d%Y")
        results = session.query(func.min(Measurements.tobs),func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start).all()

        session.close()

        return jsonify(list(np.ravel(results)))

    start=dt.datetime.strptime(start,"%m%d%Y")
    end = dt.datetime.strptime(end,"%m%d%Y")
    results = session.query(func.min(Measurements.tobs),func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    
    session.close()

    return jsonify(list(np.ravel(results)))


if __name__ == '__main__':
    app.run()
