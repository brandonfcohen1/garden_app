import requests

#url = 'http://127.0.0.1:5000/api/add'
url = 'https://cohengarden.herokuapp.com/last/1'


x = requests.get(url).json()
#pressure = x[0]['baro_pressure']
#temp = x[0]['baro_temp']

y = [x[0]['baro_temp'],x[0]['baro_pressure']]