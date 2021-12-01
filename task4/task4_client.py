import requests
import time as t
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# initializing: log the board temperature every 0.5s, starting from 0s and end at 10s
time = 0
period = 10
interval = 0.5

# Create a .txt file, and add a header
file = open('t-T.txt', 'w+')
file.write('Time,Temperature\n')
print('Logging temperature...')
print('Time,Temperature(Celsius)')

while time <= period:
    # Get temperature
    temperature = requests.get("http://192.168.4.1/sensors/temperature_sensor")
    print('{0},{1}'.format(time, temperature.json()))
    file.write('{0},{1}\n'.format(time, temperature.json()))
    t.sleep(0.5)
    time += 0.5
file.close()

#############################################################

# Read .txt as csv file
data = pd.read_csv("t-T.txt", sep=",")
# Get time data, and convert it to a float array
time_data = np.array(data.Time, dtype=float)
# Get temperature data, and convert it to a float array
temperature_data = np.array(data.Temperature, dtype=float)
# Plot temperature vs. time
plt.plot(time_data, temperature_data)
plt.ylim([22, 29])
plt.xlabel("Time(s)")
plt.ylabel(u"Temperature(\u00B0C)")
plt.title("Temperature over 10s")
plt.show()

















