from flask import Flask, jsonify, request
import random

app = Flask(__name__)
giveaways = []

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/giveaway', methods=['DELETE', 'GET'])
def giveaway():
    if request.method == "DELETE":
        giveawayId = request.json.get("id")

        if not giveawayId:             return jsonify({"message": "Failure | giveaway id required"}), 400
        if giveawayId not in giveaways: return jsonify({"message": "Failure | giveaway id not found"}), 400

        giveaways.remove(int(id))

        return jsonify({"message": "Success"}), 200
    elif request.method == "GET":

        randomgiveawayId = random.randint(0, 9999999999999999)
        
        giveaways.append(randomgiveawayId)

        return jsonify({"message": f"Success | {randomgiveawayId}"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=9472)
