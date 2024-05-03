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
    ls = data['data1']
    filename = ls['filename']
    code = ls['code']
    decode_base64(filename, code)
    return json.dumps({"result":ls}) 

@app.route('/upload', methods=['POST'])
# def upload_image():
#     try:
#         # Process the image (e.g., convert to grayscale)
#         processed_image_data = process_image()
#         # Save the processed image to a temporary file
#         filename = 'processed_image.jpg'
#         cv.imwrite(filename, processed_image_data)
#         # Return the processed image file to the client
#         return send_file(filename, mimetype='image/jpeg')
#     except Exception as e:
#         print('Error:', str(e))
#         return 'Internal server error', 500

def process_image(source):
    img = cv.imread(source)
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return gray_img

def decode_base64(filename, code):
    imgdata = base64.b64decode(code)
    filename = '../public/uploads/result/' + filename
    with open(filename, 'wb') as f:
        f.write(code)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True, use_reloader=False)
	
    