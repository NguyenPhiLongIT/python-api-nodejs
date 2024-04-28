import flask
import subprocess
import json
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app = flask.Flask(__name__, template_folder="templates")

@app.route('/pyserver', methods=['POST', 'GET'])
def call_python():
    # return render_template("index.ejs")
	subprocess.Popen(
        ['python', 'main.py'],
    )
	return 'The Python server'

if __name__ == "__main__": 
	app.run(port=5000, debug=True)