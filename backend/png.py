import folium
import osmnx as ox
from sodapy import Socrata
from math import log2
import random
import pandas as pd
import io
from html2image import Html2Image

client = Socrata("data.edmonton.ca", None)

STOPS = '4vt2-8zrq'
TRIPS = 'ctwr-tvrd'
SCHEDULE = '4fvt-p2se'

EDMONTON_BLUE = '#035086'
COLORS=['#E21E26', #Red
        '#EE8C24', #Orange
        '#F8DB44', #Yellow
        '#107547', #Dark Green
        '#68C079', #Dark Green
        '#2D63AF', #Dark Blue
        '#5CBDDE', #Light Blue 
        '#10262F', #Black
        '#99479A', #Purple 
        '#EC9195', #Pink
        '#84999A', #Grey
        '#D9EBD ', #Muted Green
        ]

def random_hex_color():
    return random.choice(COLORS)

def map_to_png(map, index):
    map.save('map.html')

    hti = Html2Image(browser='edge', custom_flags=['--virtual-time-budget=10000'])
    hti.screenshot(
        html_file='map.html', save_as=f'map{index}.png',
        size=(350, 250)
    )

def draw_stop(stop_id):
    stop = get_stop(stop_id, client)
    stop_location = [stop['geometry_point']['coordinates'][1], stop['geometry_point']['coordinates'][0]]

    m = folium.Map(location=stop_location, zoom_start=12)
    routes = get_routes_by_stop_id(stop_id, client)
    for route in routes:
        draw_route(route, client, m)
    
    folium.Marker(stop_location).add_to(m)
    return m

def draw_route(route_id, client, m):
    color = random_hex_color()
    print(f'drawing {route_id} in {color}')
    trip0 = client.get(TRIPS, route_id=route_id, direction_id=0, limit=1)
    trip1 = client.get(TRIPS, route_id=route_id, direction_id=1, limit=1)

    if len(trip0):
        trip0=trip0[0]
        points0 = trip0['geometry_line']['coordinates'][0]
        points0 = [[point[1], point[0]] for point in points0]
        add_points(points0, m, color=color)
        stops0 = get_stops_by_trip_id(trip0['trip_id'], client)
        for stop in stops0:
            s = get_stop(stop['stop_id'], client)
            pos = [s['geometry_point']['coordinates'][1],s['geometry_point']['coordinates'][0]]
            folium.Circle(location=pos, color=EDMONTON_BLUE, fill_opacity=1, fill_color=EDMONTON_BLUE, radius=4).add_to(m)
    if len(trip1):
        trip1=trip1[0]
        points1 = trip1['geometry_line']['coordinates'][0]
        points1 = [[point[1], point[0]] for point in points1]
        add_points(points1, m, color=color)

        stops1 = get_stops_by_trip_id(trip1['trip_id'], client)

        for stop in stops1:
            s = get_stop(stop['stop_id'], client)
            pos = [s['geometry_point']['coordinates'][1],s['geometry_point']['coordinates'][0]]
            folium.Circle(location=pos, color=EDMONTON_BLUE, fill_opacity=1, fill_color=EDMONTON_BLUE, radius=4).add_to(m)

def get_stop(stop_id, client):
    return client.get(STOPS, stop_id=stop_id, limit=1)[0]

def get_stops_by_trip_id(trip_id, client):
    return client.get(SCHEDULE, trip_id=trip_id)

def get_trips_by_route_id(route_id, client):
    return client.get(TRIPS, route_id=route_id)

def get_trips_by_trip_id(trip_id, client):
    return client.get(TRIPS, trip_id=trip_id)

def get_routes_by_stop_id(stop_id, client):
    results = client.get(SCHEDULE, stop_id=stop_id)
    result_df = pd.DataFrame.from_records(results)
    routes = result_df['route_id'].unique()
    return routes 

def add_points(points, m, color=random_hex_color()):
    folium.PolyLine(locations=points, color=color).add_to(m)