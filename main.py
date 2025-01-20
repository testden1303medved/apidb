from flask import Flask, jsonify, request
import random

app = Flask(__name__)
giveways = []

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/giveway', methods=['DELETE', 'GET'])
def giveaway():
    if request.method == "DELETE":
        givewayId = request.json.get("id")

        if not givewayId:             return jsonify({"message": "Failure | Giveway id required"}), 400
        if givewayId not in giveways: return jsonify({"message": "Failure | Giveway id not found"}), 400

        giveways.remove(int(id))

        return jsonify({"message": "Success"}), 200
    elif request.method == "GET":

        randomGivewayId = random.randint(0, 999999999)
        while randomGivewayId not in giveways:
            randomGivewayId = random.randint(0, 999999999)
        
        giveways.append(randomGivewayId)

        return jsonify({"message": f"Success | {randomGivewayId}"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
