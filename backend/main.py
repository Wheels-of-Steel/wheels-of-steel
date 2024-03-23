from flask import Flask, request, render_template, Response, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

@app.route("/")
def hello_world():
    return{'greeting': 'hello world!'}
