from flask import Flask, jsonify, request
from tinydb import TinyDB, Query

app = Flask(__name__)

# Initialize TinyDB
db = TinyDB('db.json')  # This will create a db.json file in your current directory
User  = Query()

# Create a new user
@app.route('/user', methods=['POST'])
def create_user():
    user_id = request.json.get('userId')
    user_data = request.json.get('data')

    if db.search(User.userId == user_id):
        return jsonify({"error": "User  ID already exists"}), 400

    db.insert({'userId': user_id, 'data': user_data})
    return jsonify({"message": "User  created", "userId": user_id}), 201

# Get user data by user ID
@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user_entry = db.search(User.userId == user_id)
    if not user_entry:
        return jsonify({"error": "User  not found"}), 404
    return jsonify({"userId": user_entry[0]['userId'], "data": user_entry[0]['data']}), 200

# Update user data
@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json.get('data')

    if not db.search(User.userId == user_id):
        return jsonify({"error": "User  not found"}), 404

    db.update({'data': user_data}, User.userId == user_id)
    return jsonify({"message": "User  updated", "userId": user_id}), 200

# Delete a user
@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not db.search(User.userId == user_id):
        return jsonify({"error": "User  not found"}), 404

    db.remove(User.userId == user_id)
    return jsonify({"message": "User  deleted", "userId": user_id}), 200

if __name__ == '__main__':
    app.run(debug=False)