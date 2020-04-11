from flask import (
    make_response,
    abort,
)
from config import db
from models import (
    Readings,
    ReadingsSchema
)

def read_all():
    """
    This function responds to a request for /api/readings
    with the complete lists of people

    :return:        json string of list of people
    """
    # Create the list of people from our data
    readings = Readings.query \
        .order_by(Readings.time) \
        .all()

    # Serialize the data for the response
    readings_schema = ReadingsSchema(many=True)
    return readings_schema.dump(readings)


def create(readings):
    """
    This function creates a new reading in the readings structure
    based on the passed-in readings data

    :param person:  reading to create in readings structure
    :return:        201 on success
    """

    # Create a person instance using the schema and the passed-in person
    schema = ReadingsSchema()
    new_reading = schema.load(readings, session=db.session)

    # Add the person to the database
    db.session.add(new_reading)
    db.session.commit()

    # Serialize and return the newly created person in the response
    return schema.dump(new_reading), 201
