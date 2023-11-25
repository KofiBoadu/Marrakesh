from flask import Blueprint

email_customers = Blueprint('send_emails', __name__,template_folder='templates', static_folder='static')


from . import routes
