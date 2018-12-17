"""
Main.routes
    home(): /, /home
    about(): /about
"""

from flask import render_template, request, Blueprint
from timexlog.models import Post

"""
Imports:
    Flask
        Blueprints to modularize the webapp
        render_template to render the html form (ie. home.html, about.html...)
        request to GET http arguments
    timexlog.models:
        User and Post entity class

"""

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    """Home route and render form"""
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('main/home.html')


@main.route("/about")
def about():
    """About route and render form"""
    return render_template('main/about.html', title='About')
