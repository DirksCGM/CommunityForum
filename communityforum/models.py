from datetime import datetime

from flask_login import UserMixin

from communityforum import db, login_manager


# takes user id and loads it to session, it manages our session for us
# we inherit UserMixin with a model that this decorator is expecting
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.String(225), nullable=True, default=' ')
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    admin = db.Column(db.Boolean(), nullable=False, default=False)

    # one to may from user to post model
    posts = db.relationship('Post', backref='author', lazy=True)

    # how object is returned
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # add user id for posts to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Communities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.DateTime(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# Add Models to Database in Project using Terminal
#   from communityforum import db
#   from communityforum.models import User, Post
#   db.create_all()
