from flask import Flask, jsonify, request
from random import randint
import json
import os

app = Flask(__name__)

class Database:
    def __init__(self, pathtofile):
        self.pathtofile = os.path.join(os.path.dirname(__file__), pathtofile)
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.pathtofile):
            with open(self.pathtofile, "w") as f:
                json.dump({}, f, indent=4)  # Initialize with an empty dictionary

    def _read(self):
        with open(self.pathtofile, "r") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.pathtofile, "w") as f:
            json.dump(data, f, indent=4)

    def add(self, key, value):
        data = self._read()
        if key not in data:
            data[key] = value
            self._write(data)

    def search(self, query):
        data = self._read()
        return {key: value for key, value in data.items() if query in key}

    def remove(self, query):
        data = self._read()
        if query in data:
            del data[query]
            self._write(data)

_customs = Database("customs.json")
_balance = Database("balance.json")

memory = []

def generate_id():
    while True:
        randstr = f"{randint(1000,9999)}-{randint(1000,9999)}-{randint(1000,9999)}-{randint(1000,9999)}"
        if randstr not in memory:
            return randstr

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/giveaways', methods=['GET', 'DELETE'])
def giveaways():
    if request.method == "GET":
        GWID = generate_id()
        memory.append(GWID)
        return jsonify({"message": f"{GWID}"}), 200

    elif request.method == "DELETE":
        GWID = request.json.get("GWID")
        if not GWID:
            return jsonify({"message": "GWID required"}), 400
        if GWID not in memory:
            return jsonify({"message": "GWID not found"}), 400
        memory.remove(GWID)
        return jsonify({"message": ""}), 200

@app.route('/tickets', methods=['GET', 'DELETE'])
def tickets():
    if request.method == "GET":
        TKID = generate_id()
        memory.append(TKID)
        return jsonify({"message": f"{TKID}"}), 200

    elif request.method == "DELETE":
        TKID = request.json.get("TKID")
        if not TKID:
            return jsonify({"message": "TKID required"}), 400
        if TKID not in memory:
            return jsonify({"message": "TKID not found"}), 400
        memory.remove(TKID)
        return jsonify({"message": ""}), 200

@app.route('/roles', methods=['GET', 'POST', 'DELETE'])
def customroles():
    if request.method == "GET":
        userId = request.args.get("userId")
        if not userId:
            return jsonify({"message": "userId required"}), 400

        users = _customs.search(userId)
        if not users:
            return jsonify({"message": "userId not found"}), 404

        return jsonify(users), 200

    if request.method == "POST":
        userId = request.json.get("userId")
        roleId = request.json.get("roleId")

        if not userId:
            return jsonify({"message": "userId required"}), 400
        if not roleId:
            return jsonify({"message": "roleId required"}), 400
        
        user = _customs.search(userId)
        if user:
            return jsonify({"message": "Role already exists for user"}), 409

        _customs.add(userId, roleId)
        return jsonify({"message": "Role added successfully"}), 201

    if request.method == "DELETE":
        userId = request.json.get("userId")

        if not userId:
            return jsonify({"message": "userId required"}), 400

        user = _customs.search(userId)
        if not user:
            return jsonify({"message": "userId not found"}), 404

        _customs.remove(userId)
        return jsonify({"message": "Role removed successfully"}), 200

@app.route('/balance', methods=['GET', 'POST', 'DELETE'])
def balance():
    if request.method == "GET":
        userId = request.args.get("userId")
        if not userId:
            return jsonify({"message": "userId required"}), 400

        balance_data = _balance.search(userId)
        if userId not in balance_data:
            return jsonify({"message": "userId not found"}), 404

        return jsonify({userId: balance_data[userId]}), 200

    if request.method == "POST":
        userId = request.json.get("userId")
        amount = request.json.get("amount")

        if not userId:
            return jsonify({"message": "userId required"}), 400
        if amount is None:
            return jsonify({"message": "amount required"}), 400

        balance_data = _balance._read()
        if userId in balance_data:
            # Update existing balance
            balance_data[userId] += amount
        else:
            # Add new user with initial balance
            balance_data[userId] = amount

        _balance._write(balance_data)
        return jsonify({"message": "Balance updated successfully"}), 200

    if request.method == "DELETE":
        userId = request.json.get("userId")

        if not userId:
            return jsonify({"message": "userId required"}), 400

        balance_data = _balance._read()
        if userId not in balance_data:
            return jsonify({"message": "userId not found"}), 404

        del balance_data[userId]
        _balance._write(balance_data)
        return jsonify({"message": "User  balance removed successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
