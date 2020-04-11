# Data to serve with our API
READINGS = {
    "1": {
            "baro_temp":76,
            "baro_pressure":30.5,
            "cpu_temp":110,
            "humid_temp":75,
            "humid_humid":50,
            "light":0,
            "time":100,
        }
}

# Create a handler for our read (GET) people
def read():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        sorted list of people
    """
    # Create the list of people from our data
    return [READINGS[key] for key in sorted(READINGS.keys())]
