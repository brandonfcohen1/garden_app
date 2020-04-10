import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('result.csv')

#plt.plot(data['temp'])
plt.plot(data['motion'])
#plt.plot(data['cpu_temp'])
plt.show()