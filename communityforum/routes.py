from flask import render_template, flash, redirect, url_for

from communityforum import app
from communityforum.forms import RegistrationForm, LoginForm
from communityforum.models import User, Post

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
