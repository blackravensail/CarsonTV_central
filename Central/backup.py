from flask import Flask, request, make_response
import json

app = Flask(__name__)


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
app.after_request(add_cors_headers)

with open("/home/blakewintermute/mysite/titles.json","r") as f:
    titleList = json.load(f)
with open("/home/blakewintermute/mysite/userData.json","r") as f:
    userData = json.load(f)


@app.route('/json')
def get_json():
    userID = request.args.get("UserID")

    if userID == "master":
        return titleList

    if userID not in userData:
        return "Not a User", 401

    titles = {}

    for id in userData[userID]["titles"]:
        titles[id] = titleList[id]

    r = make_response(json.dumps({"titles":titles, "pdata":userData[userID]["pdata"], "serverList": userData[userID]["servers"]}))
    #r.headers.add('Access-Control-Allow-Origin', '*')
    r.headers['Access-Control-Allow-Origin'] = "*"
    return r


@app.route('/update', methods=['POST'])
def updateProgress():
    update = json.loads(request.get_data())
    uid = update["UserID"]

    if uid not in userData:
        return str(uid) + ' is not a user', 401

    id = update["id"]
    if titleList[id]["type"] == "series":
        cS = update["cS"]
        cE = update["cE"]
        if id not in userData[uid]["pdata"]:
            userData[uid]["pdata"][id] = {"cE":0, "cS":0, "map":{}}

        userData[uid]["pdata"][id]["cS"] = cS
        userData[uid]["pdata"][id]["cE"] = cE

        if str(cS) not in userData[uid]["pdata"][id]["map"]:
            userData[uid]["pdata"][id]["map"][str(cS)] = {}

        userData[uid]["pdata"][id]["map"][str(cS)][str(cE)] = update["progress"]
    else:
        userData[uid]["pdata"][id] = update["progress"]

    with open("/home/blakewintermute/mysite/userData.json", "w") as f:
        json.dump(userData, f)
    return '', 200


@app.route('/')
def default():
    return "Hi, this is the JSON server for CarsonTV"
