from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import desc,asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET','POST'])
def messages():
    
    
    messages = Message.query.order_by(asc(Message.created_at))

    if request.method == 'GET':
        messages_list=[]
        for message in messages:
            message_dict=message.to_dict()
            messages_list.append(message_dict)

        response = make_response(jsonify(messages_list),200)

        return response
    elif request.method == 'POST':
        requesto = request.get_json()
        new_message = Message(
            body = requesto.get("body"),
            username = requesto.get("username"),
            
            
        )
        
        
        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            jsonify(message_dict),
            201
        )

        return response

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()
    
    if request.method == 'GET':
        message_dict=message.to_dict()
       

        response = make_response(jsonify(message_dict),200)

        return response
    
    elif request.method == 'PATCH':
        requesto = request.get_json()
        
        for attr in requesto:
            setattr(message, attr, requesto.get(attr))
            
        db.session.add(message)
        db.session.commit()
        
        message_dict= message.to_dict()
        
        response = make_response(
                jsonify(message_dict),
                200
            )

        return response
    
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
