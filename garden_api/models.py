from datetime import datetime
from config import db, ma

class Readings(db.Model):
    __tablename__ = 'readings'
    reading_id =  db.Column(db.Integer, primary_key=True)
    baro_temp = db.Column(db.Float)
    baro_pressure = db.Column(db.Float)
    cpu_temp = db.Column(db.Float)
    humid_temp = db.Column(db.Float)
    humid_humid = db.Column(db.Float)
    light = db.Column(db.Integer)
    time = db.Column(db.Float)
