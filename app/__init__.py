from flask import Flask,redirect,url_for
from .customers import customers_bp  # Import the Blueprint from the customers module
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__,static_folder='static')

    @app.route('/')
    def redirect_to_customers():
        return redirect(url_for('customers.home_page'))

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.secret_key = os.getenv('SECRET_KEY')

    return app

