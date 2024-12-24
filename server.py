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

# Serve React App - Handle all routes


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Error handler for 404


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')
