from flask  import Flask, jsonify, request
from random import *

app = Flask(__name__)

class Handler():
    def __init__(self):
        self.db = []

    def add(self, data): self.db.append(data)
    def rem(self, data): self.db.remove(data)

    def generateId(self) -> str:
        while True:
            randstr = f"{randint(1000,9999)}-{randint(1000,9999)}-{randint(1000,9999)}-{randint(1000,9999)}"
            if randstr not in self.db:
                return randstr
    
hand = Handler()

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/giveaways', methods=['GET', 'DELETE'])
def gws():
    if request.method == "GET":
        
        GWID = hand.generateId()
        hand.add(GWID)

        return jsonify({"message": f"{GWID}"}), 200

    elif request.method == "DELETE":
        GWID = request.json.get("GWID")

        if not GWID:            return jsonify({"message": "GWID required"}), 400
        if GWID not in hand.db: return jsonify({"message": "GWID not found"}), 400

        hand.rem(GWID)

        return jsonify({"message": ""}), 200

@app.route('/tickets', methods=['GET', 'DELETE'])
def tks():
    if request.method == "GET":
        
        TKID = hand.generateId()
        hand.add(TKID)

        return jsonify({"message": f"{TKID}"}), 200

    elif request.method == "DELETE":
        TKID = request.json.get("TKID")

        if not TKID:            return jsonify({"message": "TKID required"}), 400
        if TKID not in hand.db: return jsonify({"message": "TKID not found"}), 400

        hand.rem(TKID)

        return jsonify({"message": ""}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
