from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    given_name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    posts = db.relationship('UserPost', backref='user', lazy=True)
    post_likes = db.relationship('PostLike', backref='user', lazy=True)
    post_comments = db.relationship('PostComment', backref='user', lazy=True)

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_request = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    profile_accept = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    request_user = db.relationship('UserProfile', foreign_keys=[profile_request], backref='requested_friendships')
    accept_user = db.relationship('UserProfile', foreign_keys=[profile_accept], backref='accepted_friendships')

class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    written_text = db.Column(db.Text, nullable=True)
    media_location = db.Column(db.Text, nullable=True)
    created_datetime = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    likes = db.relationship('PostLike', backref='post', lazy=True)
    comments = db.relationship('PostComment', backref='post', lazy=True)

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('user_post.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class PostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('user_post.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
