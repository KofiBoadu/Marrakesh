from flask import Flask, redirect, url_for,session
from app.extension import login_manager, cache
from .customers import customers_bp
from app.users import users_bp
from dotenv import load_dotenv
import os
from .customer_profiles import customers_profile
from  .send_emails import email_customers
from .emails import mail






def create_app():
    load_dotenv()
    app = Flask(__name__,static_folder='static')

    @app.route('/')
    def redirect_to_login():
        return redirect(url_for('users.login'))

    @app.context_processor
    def inject_user():
        username = session.get('username')
        if username:
            return {'username': username}
        return {'username': None}


    app.register_blueprint(users_bp,url_prefix='/users')

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(customers_profile, url_prefix='/profiles')
    app.register_blueprint(email_customers,url_prefix='/send_emails')

    app.secret_key = os.getenv('SECRET_KEY')

     # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtpout.secureserver.net'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    # app.config['REDIS_URL'] = os.environ.get('REDIS_URL', "redis://localhost:6379/0")


    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view='users.login'
    # redis_client = FlaskRedis(app)
    cache.init_app(app)
    return app






