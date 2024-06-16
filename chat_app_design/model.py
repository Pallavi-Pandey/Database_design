from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    from_number = db.Column(db.Integer, nullable=False)
    to_number = db.Column(db.Integer, nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    send_datetime = db.Column(db.DateTime, nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.conversation_id'), nullable=False)

class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    profile_photo = db.Column(db.LargeBinary, nullable=True)
    phone_no = db.Column(db.Integer, unique=True, nullable=False)

class GroupMember(db.Model):
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.contact_id'), nullable=False, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.conversation_id'), nullable=False, primary_key=True)
    joined_date = db.Column(db.DateTime, nullable=False)
    left_date = db.Column(db.DateTime, nullable=True)

class Conversation(db.Model):
    conversation_id = db.Column(db.Integer, primary_key=True)
    conversation_name = db.Column(db.String, nullable=False)
    messages = db.relationship('Message', backref='conversation', lazy=True)
    members = db.relationship('GroupMember', backref='conversation', lazy=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
