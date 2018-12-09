"""
Users.forms:
    RegistrationForm(FlaskForm)
    LoginForm(FlaskForm)
    UpdateAccountForm(FlaskForm)
    RequestResetForm(FlaskForm)
    ResetPasswordForm(FlaskForm)
Imports:
    Flask: Blueprints
    flask wt form
    flask_wtf.file: filefield, FileAllowed used in update account form
    wt.forms: fields used in forms
    wt forms: validators used in var declaratoins
    wt forms: validationerror used in custom field validation function
    flask_login: current_user used in updateaccount form
    user model: used in customr field validation function
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from timexlog.models import User


class RegistrationForm(FlaskForm):
    """
    Registration Form
    """
    username = \
        StringField('Username',
                    validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
               # todo: add minimum length
    confirm_password = \
        PasswordField('Confirm Password',
                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validation if username is unique"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose another.')

    def validate_email(self, email):
        """Validation if email is unique"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose another.')

    # Template validate field
    # def validate_field(self, field):
    #     """Validation"""
    #     if True:
    #         raise ValueError('msg')


class LoginForm(FlaskForm):
    """
    Login form
    """# username = StringField('Username',
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
                             # todo: add minimum length
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    Update User Account Form
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update account')

    def validate_username(self, username):
        """Validation if username is unique"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose another.')

    def validate_email(self, email):
        """Validation if email is unique"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please choose another.')


class RequestResetForm(FlaskForm):
    """Reset pw page to submit reset request"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account with email. register first!')


class ResetPasswordForm(FlaskForm):
    """
    Rest password form
    """
    password = PasswordField('Password', validators=[DataRequired()])
                             # todo: add minimum length
    confirm_password = \
        PasswordField('Confirm Password',
                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
