import sys
import pandas as pd
import numpy as np
from pykalman import KalmanFilter
from xml.dom.minidom import parse
import math
#python3 calc_distance.py walk1.gpx walk1.csv

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.7f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.7f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def get_data(input_gpx):
    data = parse(input_gpx)
    #parse_result.iter( '{http://www.topografix.com/GPX/1/0}trkpt' )
    trkpts = data.getElementsByTagName("trkpt")
    time = []
    lat = []
    lon = []
    for trkpt in trkpts:
        times = trkpt.getElementsByTagName("time")[0].firstChild.data
        time.append(times)
        lat.append(trkpt.getAttribute('lat'))
        lon.append(trkpt.getAttribute('lon')) 
    result = pd.DataFrame({
        "datetime": time,
        "lat": lat,
        "lon": lon
    })
    result['datetime'] = pd.to_datetime(result['datetime'], utc=True)
    result['lat'] = result['lat'].astype(float)
    result['lon'] = result['lon'].astype(float)
    return result

# source: https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
def haversine(lat1, lon1, lat2, lon2):
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c * 1000

def distance(df):
    data = df.copy()
    data['shifted_lat'] = data['lat'].shift(periods = 1)
    data['shifted_lon'] = data['lon'].shift(periods = 1)
    data['dist'] = data.apply(lambda l: haversine(l['lat'], l['lon'], l['shifted_lat'], l['shifted_lon']), axis = 1)
    return data['dist'].sum()

def smooth(points):
    initial_state = points.iloc[0]
    observation_covariance = np.diag([3.2,3.2,3.2,3.2]) ** 2 
    transition_covariance = np.diag([4,4,4,4]) ** 2 
    transition = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    kf = KalmanFilter(initial_state_mean = initial_state, observation_covariance = observation_covariance, transition_covariance = transition_covariance, transition_matrices = transition)
    smoothed, _ = kf.smooth(points)
    result = pd.DataFrame(smoothed)
    result = result.rename(columns={0: "lat", 1: "lon"})
    return result



def main():
    input_gpx = sys.argv[1]
    input_csv = sys.argv[2]
    
    points = get_data(input_gpx).set_index('datetime')
    #print(points)
    sensor_data = pd.read_csv(input_csv, parse_dates=['datetime']).set_index('datetime')
    points['Bx'] = sensor_data['Bx']
    points['By'] = sensor_data['By']

    dist = distance(points)
    print(f'Unfiltered distance: {dist:.2f}')

    """ 
    point = pd.DataFrame({
    'lat': [49.28, 49.26, 49.26],
    'lon': [123.00, 123.10, 123.05]})
    print(distance(point).round(6))
    """

    smoothed_points = smooth(points)
    smoothed_dist = distance(smoothed_points)
    print(f'Filtered distance: {smoothed_dist:.2f}')

    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()
