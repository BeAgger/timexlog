"""
Blog.routes
    new_post(): /post/new
    post(post_id): /post/<int:post_id>
    user_posts(username): /post/user/<string:username>
    update_post(post_id): /post/<int:post_id>/update
    delete_post(post_id): /post/<int:post_id>/delete

Imports:
    Flask
        Blueprints
        render_template to render the html form (ie. home.html, about.html...)
        url_for to manage links properly
        flash to show messages to user
        redirect to redirect between forms and pages
        request to GET http arguments
        abort to handle abortion of code execution, used in update_post()
    flask_login:
        current_user: register and login to vheck for a logged in user
        login_required decorator to routes that needs user is logged in
    timexlog:
        db
    timexlog.models:
        Post, User entity class
    timexlog.posts.forms:
        user-defined forms: posts forms
"""

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from timexlog import db
from timexlog.models import Post, User
from timexlog.blog.forms import PostForm


blog = Blueprint('blog', __name__)


@blog.route("/blog/")
@blog.route("/blog/home")
def home():
    """Blog route and render form"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts)


@blog.route("/blog/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """Create new post"""
    form = PostForm()
    if form.validate_on_submit():
        post_new = Post(title=form.title.data, content=form.content.data, author=current_user)
        # set the author by using the backref author in stead of user_id
        db.session.add(post_new)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('blog.home'))
    return render_template('create_post.html', title="New Post",
                           form=form, legend='New Post')


@blog.route("/blog/post/<int:post_id>")
def post(post_id):
    """Show a post"""
    post_cur = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post_cur.title, post=post_cur)


@blog.route("/blog/user/<string:username>")
def user_posts(username):
    """User route and render form"""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@blog.route("/blog/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """Update a post"""
    post_upd = Post.query.get_or_404(post_id)
    # only allow edit if current user is the author
    if post_upd.author != current_user:
        abort(403)
    form = PostForm()
    # add to db if form submitted successfully
    if form.validate_on_submit():
        post_upd.title = form.title.data
        post_upd.content = form.content.data
        db.session.add(post_upd)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('blog.post', post_id=post_upd.id))
    elif request.method == 'GET':
        # else populate with current post data
        form.title.data = post_upd.title
        form.content.data = post_upd.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@blog.route("/blog/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post"""
    post_del = Post.query.get_or_404(post_id)
    if post_del.author != current_user:
        abort(403)
    db.session.delete(post_del)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('blog.home'))
    # return redirect(url_for('main.home'))


"""
@blog.route("/blog/latest")
def latest_posts():
    ""Home route and render form""
    page = request.args.get('page', 1, type=int)
    posts = Post.query\
        .order_by(Post.date_posted.desc())\
        .limit(2)\
        .paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)
"""
