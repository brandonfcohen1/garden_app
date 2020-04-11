import requests

if False:
    x = {'baro_pressure': 10.0,
        'baro_temp': 10.0,
        'cpu_temp': 10.0,
        'humid_humid': 10.0,
        'humid_temp': 10.0,
        'light': 10,
        'time': 10.0}
    
    r = requests.post('http://localhost:5000/api/readings', json = x)
    print(r.status_code)

d = requests.get('http://localhost:5000/api/readings')
