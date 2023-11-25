from flask import Flask,redirect,url_for
from .customers import customers_bp
from dotenv import load_dotenv
import os
from .customer_profiles import customers_profile
from  .send_emails import email_customers
from .emails import mail


load_dotenv()
def create_app():
    app = Flask(__name__,static_folder='static')

    @app.route('/')
    def redirect_to_customers():
        return redirect(url_for('customers.home_page'))

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(customers_profile, url_prefix='/profiles')
    app.register_blueprint(email_customers,url_prefix='/send_emails')
    app.secret_key = os.getenv('SECRET_KEY')

     # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    mail.init_app(app)

    return app

