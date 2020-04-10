import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('templog.csv')

plt.plot(data['temp'])
plt.show()