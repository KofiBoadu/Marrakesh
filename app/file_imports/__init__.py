from flask import Blueprint


fileImport_bp = Blueprint('importing', __name__,template_folder='templates', static_folder='static')

from . import routes
