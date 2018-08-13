from flask import Flask, request, send_from_directory
import os
import json
CarsonMedia = "E:\\CarsonMedia"

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/list')
def lister():
    lst = os.listdir(CarsonMedia)
    return json.dumps({"titles": lst}), 200

@app.route('/check')
def checker():
    return "Working!", 200

@app.route('/media/<path:path>')
def send_file(path):
    return send_from_directory(CarsonMedia, path)

@app.route('/')
def default():
    return "Success!"

if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', port=8082)
