import flask
# import subprocess
import json
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)
app = flask.Flask(__name__, template_folder="templates")

@app.route('/pyserver', methods=['POST', 'GET'])
def call_python():
    import cv2 # type: ignore
    im = cv2.imread('image/CoinsA.png')

    return render_template("index.ejs", imageSrc="image/CoinsA.png")

@app.route('/gallery', methods=['POST', 'GET'])
def get_gallery():
    import cv2 # type: ignore
    im_names = []
    im = cv2.imread('../public/image/CoinsA.png')
    ret1, jpeg1 = cv2.imencode('.png', im)
    print(im_names)
    im_names.append(jpeg1.tobytes())
    return render_template("gallery.html", image_names=im_names)
if __name__ == "__main__": 
	app.run(host= '0.0.0.0', port=5000, debug=True)