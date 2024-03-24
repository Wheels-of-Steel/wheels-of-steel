import folium
import osmnx as ox
from html2image import Html2Image

def map_to_png(map):
    map.save('map.html')

    hti = Html2Image(browser='edge', custom_flags=['--virtual-time-budget=10000'])
    hti.screenshot(
        html_file='map.html', save_as='map.png',
        size=(350, 250)
    )