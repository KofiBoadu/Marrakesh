from flask import Blueprint

analytics = Blueprint('analytics', __name__, template_folder='templates',static_folder='static',static_url_path='/analytics/static')

from . import routes
