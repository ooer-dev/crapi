from flask import Blueprint
from flask_restful import Api

from crapi.blueprints.api.resources.reactions import ReactionsResource, ReactionResource
from crapi.util.csrf import csrf

blueprint = Blueprint('api', __name__, url_prefix='/api')
csrf.exempt(blueprint)
api = Api(blueprint)

api.add_resource(ReactionsResource, '/reactions', endpoint='reactions')
api.add_resource(ReactionResource, '/reactions/<int:reaction_id>', endpoint='reaction')
