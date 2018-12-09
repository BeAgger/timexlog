"""
Users.routes
    register(): /register
    login(): /login
    logout(): /logout
    account(): /account
    reset_request(): /reset_password
    reset_token(token): /reset_password/<token>
Imports:
    Flask
        Blueprints
        render_template to render the html form (ie. home.html, about.html...)
        url_for to manage links properly
        flash to show messages to user
        redirect to redirect between forms and pages
        request to GET http arguments
    flask_login:
        login_user function used in login route
        current_user: register and login to vheck for a logged in user
        logout_user logout user out used in logout route
        login_required decorator to routes that needs user is logged in
    timexlog:
        db, bcrypt_flask
    timexlog.models:
        User and entity class
    timexlog.users.forms:
        user-defined forms: register, login, updateaccount, reset password forms
    timexlog.users.utils:
        save_picture and send_reset_email
"""

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from timexlog import db, bcrypt_flask
from timexlog.models import User
from timexlog.users.forms import (RegistrationForm, LoginForm,
                                   UpdateAccountForm, RequestResetForm,
                                   ResetPasswordForm)
from timexlog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
# must accept both get and post requests.
def register():
    """Register route and render form. Validate user."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    # check if form validated properly (when we come back to the form after submit)
    if form.validate_on_submit():
        hsh_pw = bcrypt_flask.generate_password_hash(form.password.data, 12).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hsh_pw, agree_conditions=form.agree_conditions.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """Login route and render form. Login user."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt_flask.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
            # flash('You have been logged in', 'success')
        else:
            flash('Access denied. Login failed!', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """Log the user out"""
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Account"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',
                         filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """Request password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with reset instructions.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Request password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hsh_pw = bcrypt_flask.generate_password_hash(form.password.data, 12).decode('utf-8')
        user.password = hsh_pw
        db.session.commit()
        flash('Password updated. Please login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
