from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='client/dist')
CORS(app)

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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
