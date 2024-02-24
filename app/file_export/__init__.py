from flask import Blueprint


fileExport_bp = Blueprint('exportingFile', __name__,template_folder='templates', static_folder='static')

from . import routes
