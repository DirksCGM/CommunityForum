from datetime import datetime

from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '1511f5d332s54a45s548f7g3g9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


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
#   from app import db
#   db.create_all()
# Add Dummy User and Post
#   from app import User, Post
#   test_user = User(username='Test User', email='test@user.com', password='123456789')
#   db.session.add(test_user)
#   db.session.commit()


posts = [
    {
        'author': 'Dude101',
        'title': 'New to the site!',
        'content': 'Hey! I am new to the site ^^',
        'date_posted': 'Apr 20 2020'
    },
    {
        'author': 'Dudette101',
        'title': 'New to the site!',
        'content': 'Hey! I am new to the site :)',
        'date_posted': 'Apr 25 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == '123456789':
            flash(f'Welcome {form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Invalid email or password!', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
