from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/pyserver', methods=['GET'])
def callApi():
    return render_template("index.ejs")

if __name__ == "__main__": 
	app.run()