from flask import Blueprint

contacts_bp = Blueprint('contacts', __name__, template_folder='templates', static_folder='static')

from . import routes
