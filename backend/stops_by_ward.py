import pandas as pd
import geopandas as gpd
import requests
from flask import request, jsonify, json
from shapely.geometry import Polygon, Point
from shapely.wkt import loads
import matplotlib.pyplot as plt

get_ward = "https://data.edmonton.ca/resource/b4er-5rp2.json?$query=SELECT%0A%20%20%60name_1%60%2C%0A%20%20%60name_2%60%2C%0A%20%20%60effective_start_date%60%2C%0A%20%20%60effective_end_date%60%2C%0A%20%20%60councillor%60%2C%0A%20%20%60councillor2%60%2C%0A%20%20%60geometry_multipolygon%60%0AWHERE%20caseless_eq(%60name_1%60%2C%20%22"
all_wards = "https://data.edmonton.ca/resource/b4er-5rp2.json?$query=SELECT%20%60geometry_multipolygon%60%2C%20%60name_1%60%0AGROUP%20BY%20%60geometry_multipolygon%60%2C%20%60name_1%60"
all_stops = "https://data.edmonton.ca/resource/4vt2-8zrq.json?$query=SELECT%20%60stop_id%60%2C%20%60geometry_point%60%20GROUP%20BY%20%60stop_id%60%2C%20%60geometry_point%60"
# Find stops in a neighbourhood by checking for stops within neighbourhood boundary

def stops_in_ward(ward_name):
    # store incoming data 
    ward_query = get_ward + ward_name + "%22)"

    response = requests.get(ward_query)

    if response.status_code == 200:
        ward_df = pd.DataFrame(json.loads(response.text))
        
        geometry_multipolygon = ward_df['geometry_multipolygon'].iloc[0]

        if isinstance(geometry_multipolygon, dict):
            coordinates = geometry_multipolygon.get('coordinates')
            coordinates = coordinates[0][0]
            if coordinates:
                #create a polygon out of the coordinates for ward
                polygon = Polygon(coordinates)

                #convert to a geodataframe
                multipolygon_gdf = gpd.GeoDataFrame({'geometry': [polygon]})

                #create a list of Point geometries and associated IDs
                ids = []
                points = []

                #fetch all stops
                file = open("data_sets/ETS_Stops.geojson",)
                stops = json.load(file)

                for feature in stops['features']:
                    properties = feature.get('properties')
                    geometry = feature.get('geometry')

                    if properties and geometry:
                        stop_id = properties.get('stop_id')
                        coordinates = geometry.get('coordinates')

                        if stop_id is not None and coordinates is not None and len(coordinates) == 2:
                            point = Point(coordinates)  # Create a Point geometry
                            ids.append(stop_id)  # Append the ID
                            points.append(point)  # Append the Point geometry

                # Create a GeoDataFrame with ID and geometry columns
                
                bus_stops_gdf = gpd.GeoDataFrame({'stop_id': ids, 'geometry': points})
                
                bus_stops_within_multipolygon = gpd.sjoin(bus_stops_gdf, multipolygon_gdf, predicate='within')

                return bus_stops_within_multipolygon.to_json()
            
        else:
            print("No MultiPolygon geometry found in the DataFrame.")
    else:
        return "Failed to fetch data from the URL"
    
    

def all_routes():

    geo_set = "https://data.edmonton.ca/resource/ctwr-tvrd.json?$query=SELECT%0A%20%20%60route_id%60%2C%0A%20%20%60direction_id%60%2C%0A%20%20%60geometry_line%60%2C%0A%20%20%60line_length%60%2C%0A%20%20%60trip_headsign%60%0AGROUP%20BY%0A%20%20%60route_id%60%2C%0A%20%20%60direction_id%60%2C%0A%20%20%60geometry_line%60%2C%0A%20%20%60line_length%60%2C%0A%20%20%60trip_headsign%60%0AHAVING%20%60direction_id%60%20%3D%200"

    response = requests.get(geo_set)

    if response.status_code == 200:
        df = pd.read_json(response.text)
        return df.to_json()
    else:
        return "Failed to fetch data from the URL"
    
