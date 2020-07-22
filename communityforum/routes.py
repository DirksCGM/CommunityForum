import datetime
import os
import re
import secrets

from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from communityforum import app, bcrypt, db
from communityforum.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommunityForm
from communityforum.models import User, Post, Communities


# FUNCTIONS    ---------------------------------------------------------------------------------------------------------
def save_picture(form_picture, directory, crop):
    random_hex = secrets.token_hex(8)  # unique name for image
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/{directory}', picture_fn)

    i = Image.open(form_picture)
    if crop:
        width, height = i.size
        # crop image
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            i = i.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            i = i.crop((left, top, right, bottom))

        # resize image
        output_size = (125, 125)
        i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


# INFO PAGES    --------------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    communities = Communities.query.all()
    posts = Post.query.all()
    new_community = db.engine.execute("""
        select distinct c.title, c.description, count(post.title) as count, c.url
        from post
                 join communities c on post.community = c.url
        where substr(post.date_posted, 0, 11) = substr(datetime('now', 'localtime'), 0, 11)
        group by 1;
    """).fetchall()

    return render_template('home.html', communities=communities, posts=posts, new_community=new_community,
                           datetime=datetime.datetime.utcnow)


@app.route('/about')
def about():
    return render_template('about.html')


# POST PAGES    --------------------------------------------------------------------------------------------------------
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        post = Post(title=form.title.data, content=form.content.data, author=current_user,
                    community=form.community.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New post', form=form,
                           legend='New Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # check if user is allowed to delete
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.community = form.community.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.community.data = post.community
    return render_template('create_post.html', title='Update post', form=form,
                           legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # check if user is allowed to delete
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


# COMMUNITY PAGES ------------------------------------------------------------------------------------------------------
@app.route('/community/<community_url>')
@login_required
def community(community_url):
    posts = Post.query.filter_by(community=community_url)
    communities = Communities.query.filter_by(url=community_url).first()
    return render_template('community.html', posts=posts, communities=communities)


@app.route('/community/new', methods=['GET', 'POST'])
@login_required
def new_community():
    form = CommunityForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'community_pics', False)
        else:
            picture_file = 'default.jpg'
        community = Communities(title=form.title.data, description=form.description.data,
                                url=re.sub(r'[^a-zA-Z ]+', '', form.title.data.lower().strip().replace(' ', '')),
                                image_file=picture_file)
        db.session.add(community)
        flash('Your community has been created!', 'success')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_community.html', title='Admin', form=form, legend='New Community')


# ACCOUNT PAGES --------------------------------------------------------------------------------------------------------

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # create new user with hashed password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # validate login credentials with db
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # grabs the page someone tried to go to but requires log in first
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Invalid email or password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # check for picture data
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'profile_pics', True)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # add current details in form for user
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
