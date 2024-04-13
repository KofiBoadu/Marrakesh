from flask import Blueprint


email_marketing= Blueprint('marketing', __name__,template_folder='templates', static_folder='static',static_url_path='/marketing/static')

from . import routes