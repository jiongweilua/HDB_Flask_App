import json
import pandas as pd
import numpy as np
import requests
import json
import sys




def OneMapSearch (search_string):
 
    url = "https://developers.onemap.sg/commonapi/search"
 
    querystring = {"searchVal": search_string, "returnGeom": "Y", "getAddrDetails": "Y", "pageNum": "1"}
 
    headers = {
        'cache-control': "no-cache",
        'postman-token': "0b1a9cd0-d6f1-6ad6-0e10-ffcdf8d8a3cf"
    }
 
    response = requests.request("GET", url, headers=headers, params=querystring)
 
    search_response_str = response.text
    search_response_json = json.loads(search_response_str)
    
    return search_response_json

def Searcher(search_string):
    search_response_json = OneMapSearch(search_string)
    if search_response_json["found"] == 1:
        return search_response_json["results"][0]
    elif search_response_json["found"] != 1:
        z = search_string.partition(" ")[2]
        search_response_json2 = OneMapSearch(z)
        try:
            if search_response_json2["found"] == 1:
                return search_response_json2["results"][0]
            elif search_response_json2["found"] == 0:
                return("Error")
            else:
                return("Error")
        except:
            return('Error')
    else:
        return("Error")

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


def compute_nearest_mrt_dist(add_lon,add_lat):
    mrt = pd.read_csv('./data/mrt_stations.csv')
    mrt = mrt[mrt['linecode']!= 'TE']
    mrt = mrt[mrt['stationcode']!= 'DT36']
    mrt = mrt.reset_index(drop = True) 
    
    for i in range(0,len(mrt)):
        mrt['distance'] = haversine_np(add_lon, add_lat, mrt['lon.mrt'], mrt['lat.mrt'])
    print(mrt.head())

    nearest_mrt_index = mrt['distance'].idxmin(axis = 0)
    nearest_mrt = mrt.loc[nearest_mrt_index,'name.mrt'] 
    nearest_mrt_dist = mrt.loc[nearest_mrt_index,'distance'] 

    return(nearest_mrt_dist)


def compute_distance_city_hall(add_lon, add_lat):
    distance = haversine_np(add_lon, add_lat, 103.85233, 1.29247)
    return(distance)