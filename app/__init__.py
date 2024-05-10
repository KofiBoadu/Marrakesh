from flask import Flask, redirect, url_for, session, render_template
from app.utils.main import login_manager, cache
from .contacts import contacts_bp
from .marketing import email_marketing
from app.users import users_bp
from dotenv import load_dotenv
import os
from .contact_profile import contacts_profile
from .send_emails import email_customers
from .utils.main import mail
from app.file_export import fileExport_bp
from app.file_imports import fileImport_bp
from app.analytics import analytics
from app.events_schedule import events
from .webhooks import api_blueprint
from flask.logging import create_logger
import logging
from datetime import timedelta


def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder='utils/templates', static_folder='utils/static', static_url_path='/static')

    logger = create_logger(app)
    logger.setLevel(logging.DEBUG)

    @app.route('/contacts/home')
    def redirect_to_login():
        return redirect(url_for('users.login'))

    @app.context_processor
    def inject_user():
        username = session.get('username')
        if username:
            return {'username': username}
        return {'username': None}

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(contacts_bp, url_prefix='/contacts')
    app.register_blueprint(contacts_profile, url_prefix='/profiles')
    app.register_blueprint(email_customers, url_prefix='/send_emails')
    app.register_blueprint(email_marketing, url_prefix='/marketing')
    app.register_blueprint(fileExport_bp, url_prefix='/exportingFile')
    app.register_blueprint(fileImport_bp, url_prefix='/importing')
    app.register_blueprint(analytics, url_prefix='/analytics')
    app.register_blueprint(events, url_prefix='/events')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtpout.secureserver.net'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    cache.init_app(app)
    return app

# marrakesh= create_app()
