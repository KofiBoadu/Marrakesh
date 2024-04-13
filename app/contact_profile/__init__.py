from flask import Blueprint


contacts_profile = Blueprint('profiles', __name__, template_folder='templates', static_folder='static',static_url_path='/contact_profile/static')

from . import routes
