import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# source: https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
def distance(city, stations):
    lat1 = city['latitude']
    lon1 = city['longitude']
    lat2 = stations['latitude']
    lon2 = stations['longitude']

    dLat = (lat2 - lat1) * np.pi / 180.0
    dLon = (lon2 - lon1) * np.pi / 180.0

    lat1 = (lat1) * np.pi / 180.0
    lat2 = (lat2) * np.pi / 180.0

    a = (pow(np.sin(dLat / 2), 2) +
         pow(np.sin(dLon / 2), 2) *
             np.cos(lat1) * np.cos(lat2))
    rad = 6371
    c = 2 * np.arcsin(np.sqrt(a))
    return rad * c          # return km

def best_tmax(city, stations):
    stations['distance'] = distance(city, stations)
    shortest_val = stations.iloc[np.argmin(stations['distance'])].avg_tmax
    return shortest_val


# python3 temperature_correlation.py stations.json.gz city_data.csv output.svg

stations = pd.read_json(sys.argv[1], lines= True)
city = pd.read_csv(sys.argv[2])
output = sys.argv[3]

stations['avg_tmax'] = stations['avg_tmax'] / 10

city['area'] = city['area'] / 1000000
city[(city['area'] > 10000)] = pd.NA
city = city.dropna()
city['density'] = city['population'] / city['area']

#dist_list = city.apply(distance, axis=1, stations=stations)
#short = city.apply(best_tmax, axis=1, stations=stations)
city['tmax'] = city.apply(best_tmax, axis=1, stations=stations)
#print(distance(51.054444,-114.066944,  49.0000,-108.3833))

#print(stations)
#print(city)
#print(dist_list)
#print(short)

plt.scatter(city['tmax'],city['density'])
plt.title("Temperature vs Population Density")
plt.xlabel("Avg Max Temperature (\u00b0C)")
plt.ylabel("Population Density (people/km\u00b2)")

plt.savefig(output)
#plt.show()