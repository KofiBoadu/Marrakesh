from flask import Blueprint


email_marketing= Blueprint('marketing', __name__,template_folder='templates', static_folder='static')

from . import routes