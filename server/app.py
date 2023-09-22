# from flask import Flask, request, make_response, jsonify
# from flask_cors import CORS
# from flask_migrate import Migrate

# from models import db, Message

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json_as_unicode = True

# CORS(app)
# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/messages', methods=['GET', 'POST'])
# def messages():
#     if request.method == 'GET':
#         messages = Message.query.order_by(Message.created_at.asc()).all()
#         return jsonify([message.serialize() for message in messages])
#     elif request.method == 'POST':
#         body = request.form.get('body')
#         username = request.form.get('username')
#         new_message = Message(body=body, username=username)
#         db.session.add(new_message)
#         db.session.commit()
#         return jsonify(new_message.serialize()), 201 

# @app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
# def messages_by_id(id):
#     message = Message.query.get(id)
#     if not message:
#         return jsonify({'error': 'Message not found'}), 404
    
#     if request.method == 'PATCH' :
#         data = request.json
#         body = data.get('body')
#         if body:
#             message.body = body
#         db.session.commit()
#         return jsonify(message.serialize())
    
#     elif request.method == 'DELETE' :
#         db.session.delete(message)
#         db.session.commit()
#         return jsonify({'message': 'Message deleted'})

# if __name__ == '__main__':
#     app.run(port=5555)

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    response_body = {}
    status = 200

    if request.method == 'GET':
        response_body = []

        message_list = Message.query.all()
        for message in message_list:
            response_body.append(message.to_dict())
         
    elif request.method == 'POST':
        new_message = Message(
          body=request.get_json()["body"],
          username=request.get_json()["username"] 
        )

        db.session.add(new_message)
        db.session.commit()

        response_body = new_message.to_dict()
        status = 201

    response = make_response(
        jsonify(response_body),
        status
    )
    return response

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    response_body = {}

    if request.method == 'PATCH':
        for attr in request.get_json():
            setattr(message, attr, request.get_json()[attr])

        db.session.add(message)
        db.session.commit()

        response_body = message.to_dict()
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted."    
        }

    response = make_response(
        jsonify(response_body),
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555)