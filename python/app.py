import os
import flask
import subprocess
import json
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import base64
import cv2 as cv

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Flask server"

@app.route("/pyserver/<image_path>", methods=['GET'])
def call_python(image_path):
    print("image path", image_path )
    subprocess.Popen(
        ['python', 'main.py',image_path],
    )
    return '1'

@app.route('/postdata', methods=['POST'])
def postdata():
    data = request.get_json() 
    print(data)
    return json.dumps({"newdata":"hereisthenewdatayouwanttosend"}) 



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True, use_reloader=False)
	
    