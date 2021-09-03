from crapi.data import ma
from crapi.models.reaction import Reaction


class ReactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reaction

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.AbsoluteURLFor('api.reaction', values=dict(reaction_id="<id>")),
            "collection": ma.AbsoluteURLFor('api.reactions'),
        }
    )


reaction_schema = ReactionSchema()
reactions_schema = ReactionSchema(many=True)
