from sqlalchemy.orm import backref
from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(), nullable = False)
    password =db.Column(db.String(80))
    bio = db.Column(db.String(255), default = 'You bio  is empty')
    image_url = db.Column(db.String(), default =' profile.jgp')
    posts = db.relationship('Posts', backref = 'author', lazy = 'dynamic')
    # comments = db.relationship('Comments', backref = 'commentator', lazy = 'dynamic')


class Posts (db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


     

    def __repr__(self):
        return '<User %r>' % self.username
    



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Comment {self.id}>'