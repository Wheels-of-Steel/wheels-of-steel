from flask import Flask, request, render_template, Response, jsonify, send_file
from flask_cors import CORS, cross_origin
from stops_by_ward import stops_in_ward
from sodapy import Socrata
import png


app = Flask(__name__)

CORS(app)

client = Socrata("data.edmonton.ca", None)

@app.route("/")
def hello_world():
    return{'greeting': 'hello world!'}

@app.route("/stops_by_ward" , methods=['GET'])
def get_stops_by_ward():
    # get the ward name from the query string
    ward_name = request.args.get('ward_name')
    ouput = stops_in_ward(ward_name)
    return ouput

@app.route("/generate_png", methods=['GET'])
def generate_png():
    stop = request.args.get('points')
    print(stop)
    # stops = ['1527']
    m = png.draw_stop(stop)
    png.map_to_png(m)

    return send_file('map0.png', mimetype='image/png')

