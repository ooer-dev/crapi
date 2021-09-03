from flask import current_app
from flask_restful import Resource, reqparse

from crapi.blueprints.api.util import authenticate_bot
from crapi.data.reaction import reaction_schema, reactions_schema
from crapi.models import db
from crapi.models.reaction import Reaction


class ReactionsResource(Resource):
    method_decorators = [authenticate_bot]

    def get(self):
        reactions = Reaction.query.all()
        return reactions_schema.dump(reactions)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('trigger', type=str, required=True)
        parser.add_argument('response', type=str, required=True)
        args = parser.parse_args()

        reaction = Reaction(
            guild_id=current_app.config.get('DISCORD_GUILD_ID'),
            trigger=args['trigger'],
            response=args['response'],
        )

        db.session.add(reaction)
        db.session.commit()

        return reaction_schema.dump(reaction)


class ReactionResource(Resource):
    method_decorators = [authenticate_bot]

    def get(self, reaction_id):
        reaction = Reaction.query.get_or_404(reaction_id)

        return reaction_schema.dump(reaction)

    def patch(self, reaction_id):
        reaction = Reaction.query.get_or_404(reaction_id)

        parser = reqparse.RequestParser()
        parser.add_argument('response', type=str)
        parser.add_argument('delete_trigger', type=bool)
        parser.add_argument('dm_response', type=bool)
        parser.add_argument('contains_anywhere', type=bool)
        args = parser.parse_args()

        if args['response'] is not None:
            reaction.response = args['response']
            reaction.has_target = '%target%' in args['response']
        if args['delete_trigger'] is not None:
            reaction.delete_trigger = args['delete_trigger']
        if args['dm_response'] is not None:
            reaction.dm_response = args['dm_response']
        if args['contains_anywhere'] is not None:
            reaction.contains_anywhere = args['contains_anywhere']

        db.session.commit()

        return reaction_schema.dump(reaction)

    def delete(self, reaction_id):
        reaction = Reaction.query.get_or_404(reaction_id)

        db.session.delete(reaction)
        db.session.commit()

        return '', 204
