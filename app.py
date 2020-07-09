from flask import Flask, render_template, flash, redirect, url_for

from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '1511f5d332s54a45s548f7g3g9'

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
