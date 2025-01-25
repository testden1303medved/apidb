from flask  import Flask, jsonify, request
from random import *

app = Flask(__name__)

class rolesHandler():
    def __init__(self):
        self.db = {
            123: 123 #userId: roleId
        }

    def add(self, user, role): self.db[int(user)] = int(role)
    def rem(self, user):       self.db.pop(int(user))

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

rh   = rolesHandler()
hand = Handler()

@app.route("/")
def index():
    return "Hello, World!"

@app.route('/giveaways', methods=['GET', 'DELETE'])
def giveaways():
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
def tickets():
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
    
@app.route('/roles', methods=['GET', 'POST', 'DELETE'])
def customroles():
    if request.method == "GET":
        userId = request.args.get("userId")
        if not userId: return jsonify({"message": "userId required"}), 400

        role = rh.get_role(userId)
        if rh.db.get(int(userId), None) is None: return jsonify({"message": "userId not found"}), 400

        return jsonify({"userId": userId, "roleId": role}), 200
    if request.method == "POST":
        userId = request.json.get("userId")
        roleId = request.json.get("roleId")

        if not userId: return jsonify({"message": "userId required"}), 400
        if not roleId: return jsonify({"message": "roleId required"}), 400

        if userId in rh.db: return jsonify({"message": ""}), 204

        rh.add(userId, roleId)
        return jsonify({"message": ""}), 200
    if request.method == "DELETE":
        userId = request.json.get("userId")
        roleId = request.json.get("roleId")

        if not userId: return jsonify({"message": "userId required"}), 400
        if not roleId: return jsonify({"message": "roleId required"}), 400

        if userId not in rh.db: return jsonify({"message": "userId not found"}), 400

        rh.rem(userId)
        return jsonify({"message": ""}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
