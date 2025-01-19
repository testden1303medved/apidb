from flask import Flask, jsonify, request

app = Flask(__name__)
rdb = []

@app.route('/giveway', methods=['POST', 'GET'])
def giveaway():
    rid = request.json.get('rid')
    if not rid: return jsonify({"error": "Role Id (rid) is required"}), 400

    if request.method == "POST":
        if rid in rdb: return jsonify(), 201
        rdb.append(rid)
        return jsonify(), 200
    elif request.method == "GET":
        if rid in rdb: return jsonify(), 200
        else: return jsonify(), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
