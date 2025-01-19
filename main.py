from flask import Flask, jsonify, request

app = Flask(__name__)
rdb  = []

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/giveway', methods=['POST', 'GET'])
def giveaway():
    rid = request.headers.get("rid")
    if not rid: return jsonify({"error": "Role Id (rid) is required"}), 400
    print(f"{rid} /// {request.method}")
    if request.method == "POST":
        if rid in rdb: return jsonify("message": ""}), 201
        rdb.append(rid)
        return jsonify("message": ""}), 200
    elif request.method == "GET":
        if rid in rdb: 
            rdb.remove(rid)
            return jsonify({"message": ""}), 200
        else: return jsonify("message": ""}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
