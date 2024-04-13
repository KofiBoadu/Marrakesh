from flask import Blueprint


events = Blueprint('events', __name__,template_folder='templates', static_folder='static',static_url_path='/events_schedule/static')

from . import routes
