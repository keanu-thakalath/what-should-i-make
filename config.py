import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = int(os.environ.get('SEND_FILE_MAX_AGE_DEFAULT', 12)) # set to 0 to prevent caching of images, CSS, and JS.
    # development only, default value for production is 12
    # this gets really annoying because to see changes in a CSS file you have to clear your browser's cached files every time

    MAIL_SERVER = os.environ.get('MAIL_SERVER') # could be localhost, google, your own mail server
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # if the mail server supports user authentication, set username and password
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = [] # list of emails to send to when an error occurs
    CUISINES = ['Italian', 'Indian', 'Chinese', 'Mexican', 'Greek', 'Japanese', 'Thai', 'Mediterannean', 'American']

