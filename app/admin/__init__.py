from flask import Blueprint
admin_bp = Blueprint('admin_bp', __name__,static_folder="../static", url_prefix="/admin_api")

from . import routes