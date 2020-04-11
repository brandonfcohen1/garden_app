import os
from config import db
from models import Readings

# Data to initialize database with
READINGS = [
    {"reading_id":0, "baro_temp":0,"baro_pressure":0, "cpu_temp":0,"humid_temp":0,"humid_humid":0,"light":0, "time":0 },
    {"reading_id":1, "baro_temp":75,"baro_pressure":30, "cpu_temp":100,"humid_temp":75,"humid_humid":50,"light":0, "time":0 }
]

# Delete database file if it exists currently
if os.path.exists('readings.db'):
    os.remove('readings.db')

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for reading in READINGS:
    r = Readings(reading_id=reading['reading_id'], baro_temp=reading['baro_temp'], baro_pressure=reading['baro_pressure'], cpu_temp=reading['cpu_temp'], humid_temp=reading['humid_temp'],humid_humid=reading['humid_humid'], light=reading['light'], time=reading['time'] )
    db.session.add(r)

db.session.commit()
