"""
App Configuration
    Config class
Imports:
    os: get environment variables
"""
import os

# Specifiy default values


class Config:
    """Config class
    Handles different configs for prod/dev sites
    """
    APP_NAME = 'Time and Expense Log'
    SECRET_KEY = '1f42b9684a5a4a362d03e287301d2ac2b2a9765ab062b5fa'
    #os.environ.get('TIMGR_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///timexlog.db'
    #os.environ.get('TIMGR_SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('TIMGR_EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('TIMGR_EMAIL_PW')
    MAIL_SENDER = os.environ.get('TIMGR_EMAIL_SENDER')