"""
Users utils
    save_picture(form_picture)
    send_reset_email(user)
Imports:
    os: used in save_picture
    secrets: used in save_picture
    PIL (Pillow): used in save_picture(), resize image
    Flask:
        url_for to manage links properly
    flask_mail: Message, used in send_mail, to send emails
    timexlog:
        current_app, mail
"""

import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from timexlog import mail


def save_picture(form_picture):
    """Save the picture"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_fn


def send_reset_email(user):
    """send email to user with reset token"""
    token = user.get_reset_token()
    msg = Message('Password reset request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    # Jinja2 template to nicer mail
    msg.body = f'''
To reset your password, click this link: {url_for('users.reset_token', token=token, _external=True)}

If you did not request this, just ignore this email!
'''
    # mail.send(msg)
