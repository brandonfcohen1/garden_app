import requests

#url = 'http://127.0.0.1:5000/api/add'
url = 'https://cohengarden.herokuapp.com/api/add'

reading = {
   "baro_pressure": 10.0,
   "baro_temp": 20.0,
   "cpu_temp": 30.0,
   "humid_humid": 0.0,
   "humid_temp": 0.0,
   "light": 0,
   "reading_id": 0,
   "time": 0.0,
   "soil_moisture": 0.0
 }

print(requests.post(url, json = reading).text)