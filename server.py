import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from flask_pymongo import PyMongo


app = Flask(__name__, static_folder='client/dist')
CORS(app)


app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

# Serve API routes


@app.route('/api/test')
def test():
    return {'message': 'API is working'}

# Serve React App


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Catch all routes to serve React Router paths


@app.route('/<path:path>')
def serve_path(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')
