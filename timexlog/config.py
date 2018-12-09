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
    SECRET_KEY = os.environ.get('TIMEX_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///timexlog.db'
    #os.environ.get('TIMEX_SQLALCHEMY_DB_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('TIMEX_EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('TIMEX_EMAIL_PW')
    MAIL_SENDER = os.environ.get('TIMEX_EMAIL_SENDER')

    RECAPTCHA_PUBLIC_KEY = os.environ.get('TIMEX_RECAPT_PUB')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('TIMEX_RECAPT_PRI')
