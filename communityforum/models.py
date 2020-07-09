from datetime import datetime

from communityforum import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

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

# Add Models to Database in Project using Terminal
#   from communityforum import db
#   from communityforum.models import User, Post
#   db.create_all()
# Add Dummy User and Post
#   from app import User, Post
#   test_user = User(username='Test User', email='test@user.com', password='123456789')
#   db.session.add(test_user)
#   db.session.commit()
#
#   user.query.all()
#   user = User.query.filter_by(username='Test User').first()
#   user.id
#   user.posts
