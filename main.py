from flask import Flask, jsonify, request
from random import randint

app = Flask(__name__)

class RolesHandler:
    def __init__(self):
        self.db = {
            123: 123  # userId: roleId
        }

    def add(self, user, role):
        self.db[int(user)] = int(role)

    def rem(self, user):
        self.db.pop(int(user))

    def get(self, user):
        return self.db.get(int(user), None)

class Handler:
    def __init__(self):
        self.db = []

    def add(self, data):
        self.db.append(data)

    def rem(self, data):
        self.db.remove(data)

    def generate_id(self) -> str:
        while True:
            randstr = f"{randint(1000,9999)}-{randint(1000,9999)}-{randint(1000,9999)}-{randint(1000,9999)}"
            if randstr not in self.db:
                return randstr

rh = RolesHandler()
hand = Handler()

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/giveaways', methods=['GET', 'DELETE'])
def giveaways():
    if request.method == "GET":
        GWID = hand.generate_id()
        hand.add(GWID)
        return jsonify({"message": f"{GWID}"}), 200

    elif request.method == "DELETE":
        GWID = request.json.get("GWID")
        if not GWID:
            return jsonify({"message": "GWID required"}), 400
        if GWID not in hand.db:
            return jsonify({"message": "GWID not found"}), 400
        hand.rem(GWID)
        return jsonify({"message": ""}), 200

@app.route('/tickets', methods=['GET', 'DELETE'])
def tickets():
    if request.method == "GET":
        TKID = hand.generate_id()
        hand.add(TKID)
        return jsonify({"message": f"{TKID}"}), 200

    elif request.method == "DELETE":
        TKID = request.json.get("TKID")
        if not TKID:
            return jsonify({"message": "TKID required"}), 400
        if TKID not in hand.db:
            return jsonify({"message": "TKID not found"}), 400
        hand.rem(TKID)
        return jsonify({"message": ""}), 200

@app.route('/roles', methods=['GET', 'POST', 'DELETE'])
def customroles():
    if request.method == "GET":
        userId = request.args.get("userId")
        if not userId:
            return jsonify({"message": "userId required"}), 400

        role = rh.get(userId)
        if role is None:
            return jsonify({"message": "userId not found"}), 404

        return jsonify({"userId": userId, "roleId": role}), 200

    if request.method == "POST":
        userId = request.json.get("userId")
        roleId = request.json.get("roleId")

        if not userId:
            return jsonify({"message": "userId required"}), 400
        if not roleId:
            return jsonify({"message": "roleId required"}), 400

        if userId in rh.db:
            return jsonify({"message": "Role already exists for user"}), 204

        rh.add(userId, roleId)
        return jsonify({"message": "Role added successfully"}), 201

    if request.method == "DELETE":
        userId = request.json.get("userId")
        roleId = request.json.get("roleId")

        if not userId:
            return jsonify({"message": "userId required"}), 400
        if not roleId:
            return jsonify({"message": "roleId required"}), 400

        if userId not in rh.db:
            return jsonify({"message": "userId not found"}), 400

        rh.rem(userId)
        return jsonify({"message": "Role removed successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
