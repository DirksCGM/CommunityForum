from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  # type of filed and file validator
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from communityforum.models import User, Communities


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)]
                           )
    email = StringField('Email',
                        validators=[DataRequired(), Email()]
                        )
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)]
                             )
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8), EqualTo('password')]
                                     )
    submit = SubmitField('Sign Up')

    # custom validation to check if user already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(min=2, max=20), Email()]
                        )
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)]
                             )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)]
                           )
    email = StringField('Email',
                        validators=[DataRequired(), Email()]
                        )
    bio = TextAreaField('Bio',
                        validators=[DataRequired(), Length(min=2, max=225)]
                        )
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # custom validation to check if user already exists
    # only run validation if the data is different to their current information
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already exists.')


class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()]
                            )
    community = SelectField('Community',
                            choices=set(zip([c.url for c in Communities.query.all()], [c.title for c in Communities.query.all()])),
                            validators=[DataRequired()])
    submit = SubmitField('Post')


class CommunityForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    description = TextAreaField('Description',
                                validators=[DataRequired()]
                                )
    picture = FileField('Add Community Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create')
