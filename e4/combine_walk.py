import os
import pathlib
import sys
import numpy as np
import pandas as pd
from xml.dom.minidom import parse



def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation, parse
    xmlns = 'http://www.topografix.com/GPX/1/0'
    
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.10f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.10f' % (pt['lon']))
        time = doc.createElement('time')
        time.appendChild(doc.createTextNode(pt['timestamp'].strftime("%Y-%m-%dT%H:%M:%SZ")))
        trkpt.appendChild(time)
        trkseg.appendChild(trkpt)

    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    doc.documentElement.setAttribute('xmlns', xmlns)

    with open(output_filename, 'w') as fh:
        fh.write(doc.toprettyxml(indent='  '))


def get_data(input_gpx):
    # TODO: you may use your code from exercise 3 here.
    
    input_gpx = str(input_gpx)
    data = parse(input_gpx)
    #data = data.documentElement
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
        "timestamp": time,
        "lat": lat,
        "lon": lon,
    })
    result['timestamp'] = pd.to_datetime(result['timestamp'], errors="coerce", utc=True)
    result['lat'] = result['lat'].astype(float)
    result['lon'] = result['lon'].astype(float)
    #print(result)
    
    return result


# python3 combine_walk.py walk1 output

def main():
    input_directory = pathlib.Path(sys.argv[1])
    output_directory = pathlib.Path(sys.argv[2])
    
    accl = pd.read_json(input_directory / 'accl.ndjson.gz', lines=True, convert_dates=['timestamp'])[['timestamp', 'x']]
    gps = get_data(input_directory / 'gopro.gpx')
    phone = pd.read_csv(input_directory / 'phone.csv.gz')[['time', 'gFx', 'Bx', 'By']]

    # TODO: create "combined" as described in the exercise

    """
    first_time = accl['timestamp'].min()
    accl['rounded_timestamp'] = accl['timestamp'].dt.round('4s')
    #phone['rounded_timestamp'] = phone['time'].dt.round('4s')
    phone[ 'timestamp' ] = first_time + pd.to_timedelta(phone[ 'time' ], unit= 'sec' )
    phone_avg = phone.groupby(pd.Grouper(key='timestamp', freq='4s')).mean()

    best_offset = None

    for offset in np.linspace(-5.0, 5.0, 101):
        pass

    """

    offsets = np.linspace(-5.0, 5.0, 101)
    crossCorr = []
    first_time = accl['timestamp'].min()
    accl['timestamp'] = accl['timestamp'].dt.round("4s")
    gps['timestamp'] = gps['timestamp'].dt.round("4s")

    accl_ave = accl.groupby(['timestamp']).mean().reset_index()
    gps_ave = gps.groupby(['timestamp']).mean().reset_index()

    for offset in offsets:
        phone['timestamp'] = first_time + pd.to_timedelta(phone['time']+offset, unit='sec')
        phone['timestamp'] = phone['timestamp'].dt.round("4s")
        phone_ave = phone.groupby(['timestamp']).mean().reset_index()
        
        data = pd.merge(phone_ave, gps_ave, how='inner', left_on='timestamp', right_on='timestamp')
        data = pd.merge(data, accl_ave, how='inner', left_on='timestamp', right_on='timestamp')

        result = (data['gFx'] * data['x']).sum()
        crossCorr.append(result)
    best_offset = offsets[np.where(crossCorr == np.max(crossCorr))[0][0]]

    #print (best_offset)
    #print(accl)
    #print(gps)
    #print(phone)
    #print(data)
    
    phone['timestamp'] = first_time + pd.to_timedelta(phone['time']+best_offset, unit='sec')
    phone['timestamp'] = phone['timestamp'].dt.round("4s")
    phone_ave2 = phone.groupby(['timestamp']).mean().reset_index()
    data2 = pd.merge(phone_ave2, gps_ave, how='inner', left_on='timestamp', right_on='timestamp')
    data2 = pd.merge(data2, accl_ave, how='inner', left_on='timestamp', right_on='timestamp')
    
    #print(data2)
    
    print(f'Best time offset: {best_offset:.1f}')
    os.makedirs(output_directory, exist_ok=True)
    output_gpx(data2[['timestamp', 'lat', 'lon']], output_directory / 'walk.gpx')
    data2[['timestamp', 'Bx', 'By']].to_csv(output_directory / 'walk.csv', index=False)


main()
