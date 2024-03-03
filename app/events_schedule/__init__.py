from flask import Blueprint


events = Blueprint('events', __name__,template_folder='templates', static_folder='static')

from . import routes
