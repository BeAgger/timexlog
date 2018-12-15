"""
Timelog.forms:
    TimelogForm(FlaskForm)
Imports:
    Flask
        Blueprints
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeField, DecimalField, \
                    StringField, SubmitField
from wtforms.validators import DataRequired


class TimelogForm(FlaskForm):
    """Show time entries"""
    customer = StringField('Customer', validators=[DataRequired()])
    project = StringField('Project', validators=[DataRequired()])
    task = StringField('Task')
    datetime_start = DateTimeField('Start', format='%Y-%m-%d %H:%M:%S',\
                                   validators=[DataRequired()])
    datetime_end = DateTimeField('End', format='%Y-%m-%d %H:%M:%S')
    time_correction = DecimalField('Hours Correction')
    billable = BooleanField('Billable')
    comment = StringField('Comment')
    closed = BooleanField('Closed')
    submit = SubmitField('Add')
