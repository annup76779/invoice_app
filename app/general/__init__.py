from flask import Blueprint
general_bp = Blueprint('general_bp', __name__,static_folder="../static", url_prefix="/api")

from . import routes