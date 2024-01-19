import pandas as pd
import numpy as np
import sys
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter 

# python3 smooth_temperature.py sysinfo.csv
#def to_timestamp(x):
#   return x.timestamp()

filename = sys.argv[1]
cpu_data = pd.read_csv(filename, parse_dates = ['timestamp'])
#cpu_data['timestamp'] = cpu_data['timestamp'].apply(to_timestamp)
timestamp = cpu_data['timestamp'].apply(np.datetime64)
temperature = cpu_data['temperature'].astype(float)
#print(temperature)

#filtered = lowess(measurements, input_range, frac=0.05)
lowess = sm.nonparametric.lowess
loess_smoothed = lowess(temperature,timestamp,frac = 0.04)
#plt.show()

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0.5,0.5,0.5,0.5]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.02, 0.02, 0.02, 0.02]) ** 2 # TODO: shouldn't be zero
transition = [[1,0.7,0.1,0], [0.1,1.5,1.2,0], [0,0,1,0], [0,0,0,1]] # TODO: shouldn't (all) be zero

kf = KalmanFilter(initial_state_mean = initial_state, observation_covariance = observation_covariance, transition_covariance = transition_covariance, transition_matrices = transition)
kalman_smoothed, _ = kf.smooth(kalman_data)

plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')

plt.legend(['Data Points', 'Loess Smoothed', 'Kalman Smoothed'])
plt.title('CPU temperature')
plt.xlabel('Time')
plt.ylabel('Temperature(C)')
#plt.show() # maybe easier for testing
plt.savefig('cpu.svg') # for final submission