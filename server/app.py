from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return [message.to_dict() for message in messages]

@app.route('/messages', methods = ['POST'])
def create_message():
    data = request.get_json()
    if not data or 'body' not in data or 'username' not in data:
        abort(400, 'Invalid Input')
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()

    return new_message.to_dict(), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_messages(id):
    data = request.get_json()
    message = db.session.get(Message, id)
    if not message:
        return jsonify({"Error": "Message not found"}), 404  # Added error handling for message not found
    if "body" in data:
        message.body = data['body']
        message.updated_at = datetime.utcnow()
    db.session.commit()
    return message.to_dict(), 200

@app.route('/messages/<int:id>', methods = ['DELETE'])
def delete_messages_by_id(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({'Error': 'Message not found'}), 404  # Handle message not found
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message successfully deleted'}), 200

if __name__ == '__main__':
    app.run(port=5555)

