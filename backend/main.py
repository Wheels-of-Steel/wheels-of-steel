from flask import Flask, request, render_template, Response, jsonify
from flask_cors import CORS, cross_origin
from stops_by_ward import stops_in_ward


app = Flask(__name__)

CORS(app)

@app.route("/")
def hello_world():
    return{'greeting': 'hello world!'}

@app.route("/stops_by_ward" , methods=['GET'])
def get_stops_by_ward():
    # get the ward name from the query string
    ward_name = request.args.get('ward_name')
    ouput = stops_in_ward(ward_name)
    return ouput

