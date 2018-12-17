"""
Timelog.routes
    dashboard
    user_timelogs(username): /timelog/user/<string:username>
    add_timelog(): /timelog/new
    update_timelog(timelog_id): /timelog/<int:timelog_id>/update
    delete_timelog(timelog_id): /timelog/<int:timelog_id>/delete

Imports:
    Flask
        Blueprints
"""
from flask import (render_template, url_for, flash, redirect,
                   request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
from timexlog import db
from timexlog.models import Timelog, User
from timexlog.timelog.forms import TimelogForm

timelog = Blueprint('timelog', __name__)


@timelog.route("/timelog/")
@timelog.route("/timelog/home")
@login_required
def home():
    """Blog route and render form"""
    # page = request.args.get('page', 1, type=int)
    user = current_user
    tmlogs = Timelog.query.order_by(Timelog.datetime_start.desc())
        #.paginate(page=page, per_page=5)
    # if tmlogs.author != current_user:
    #     abort(403)
    return render_template('timelog/timelog.html', timelogs=tmlogs, user=user)


@timelog.route("/timelog/update", methods=['POST'])
@login_required
def update():
    """Update json from ajax"""
    tmlog = Timelog.query.filter_by(id=request.form['id']).first()
    tmlog.customer = request.form['customer']
    tmlog.project = request.form['project']
    tmlog.task = request.form['task']
    # tmlog.datetime_start = request.form['datetime_start']
    tmlog.comment = request.form['comment']

    db.session.commit()
    return jsonify({'result':'success'}) #, 'customer':tmlog.customer, 'project':tmlog.project})


@timelog.route("/timelog/dashboard")
@login_required
def dashboard():
    """Blog route and render form"""
    # page = request.args.get('page', 1, type=int)
    tmlogs = Timelog.query.order_by(Timelog.datetime_start.desc())
        #.paginate(page=page, per_page=5)
    return render_template('timelog/dashboard.html', timelogs=tmlogs)


@timelog.route("/timelog/add", methods=['GET', 'POST'])
@login_required
def add():
    """TimelogForm"""
    form = TimelogForm()
    # if form.validate_on_submit():
    #     timelog_new = Timelog(title=form.title.data, author=current_user)
    #     # set the author by using the backref author in stead of user_id
    #     db.session.add(timelog_new)
    #     db.session.commit()
    #     flash('Your timelog has been created.', 'success')
    #     return redirect(url_for('timelog'))
    return render_template('timelog/add_timelog.html', title="Add Timelog",
                           form=form, legend='Add Timelog')

"""
    customer = StringField('Customer', validators=[DataRequired()])
    project = StringField('Project', validators=[DataRequired()])
    task = StringField('Task')
    datetime_start = DateTimeField('Start', format='%Y-%m-%d %H:%M:%S',\
                                   validators=[DataRequired()])
    datetime_end = StringField('End', format='%Y-%m-%d %H:%M:%S')
    time_correction = DecimalField('Hours Correction')
    billable = BooleanField('Billable')
    comment = StringField('Comment')
    closed = BooleanField('Closed')
"""
