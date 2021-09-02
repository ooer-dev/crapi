from flask import Blueprint
from flask_login import LoginManager

from crapi.models.user import User

login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.login_message = u'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()


blueprint = Blueprint('auth', __name__, url_prefix='/auth/')

from crapi.blueprints.auth.views import login, logout
