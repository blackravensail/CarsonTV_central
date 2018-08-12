from flask import Flask, request, send_from_directory

CarsonMedia = ""

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/list')
def checker():
    lst = os.listdir(CarsonMedia)
    return json.dumps({"titles": lst}), 200

@app.route('/check')
def checker():
    return "Working!", 200

@app.route('/<path:path>')
def send_file(path):
    return send_from_directory(CarsonMedia, path)

if __name__ == "__main__":
    app.run()