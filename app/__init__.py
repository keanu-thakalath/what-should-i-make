from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_minify import minify
from flask_whooshee import Whooshee
from flask_login import LoginManager
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
minify = minify(html=True, js=True)
whooshee = Whooshee()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ''

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    minify.init_app(app)
    whooshee.init_app(app)
    login.init_app(app)

    # import all the blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # only email and log if in production
    if not app.debug and not app.testing:
        # if there is a mail server set up then configure email notifications
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Application Failure',
                credentials=auth, secure=secure)
            # only mail on critical errors
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
            # when an error occurs, the app will log into MAIL_SERVER as MAIL_USERNAME, MAIL_PASSWORD, then email everyone in the admins list

        # set up log error handler
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

    return app

# to avoid circular imports, import models.py down here
from app import models
