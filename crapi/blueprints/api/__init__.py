from flask import Blueprint
from flask_restful import Api

from crapi.util.csrf import csrf

blueprint = Blueprint('api', __name__, url_prefix='/api')
csrf.exempt(blueprint)
api = Api(blueprint)
