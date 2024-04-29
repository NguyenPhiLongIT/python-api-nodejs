import os
import flask
import subprocess
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)
app = flask.Flask(__name__, template_folder="templates")
# Receiving the input text from the user
@app.route("/pyserver/<image_path>", methods=['GET'])
def call_python(image_path):
    print("image path", image_path )
    subprocess.Popen(
        ['python', 'main.py',image_path],
    )
    return '1'


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True, use_reloader=False)
	
    