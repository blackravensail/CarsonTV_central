from flask import Flask, jsonify, request
app = Flask(__name__)
import json
import time

pointers = {}

@app.route('/json')
def get_incomes():
    id = request.cookies.get('UserID')
    if id not in pointers:
        with open(id + ".json",'r') as f:
            pointers[id] = json.load(f)
    return "data = " + json.dumps(pointers[id])


@app.route('/update', methods=['POST'])
def updateProgress():
    id = request.cookies.get('userID')
    update = request.get_json()
    if update["type"] == "series1":
        pointers[id]["series"][update[titleIndex]]["cS"] = update["cS"]
        pointers[id]["series"][update[titleIndex]]["cE"] = update["cE"]
    elif update["type"] == "series2":
        pointers[id]["series"][update[titleIndex]]["ep_map"][update["cS"]]["episodes"][update["cE"]]["progress"] = update["progress"]
    else:
        pointers[id]["movies"][update["titleIndex"]]["progress"] = update["progress"]
    with open(id+".json", "w") as f:
        json.dump(pointers[id], f)
    return '', 200

app.run(debug=True)
