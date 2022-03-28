import graphene
from . import mutations, queries


class Mutations(graphene.ObjectType):
    auth_by_code = mutations.AuthMutation.Field()
    pass


class Query(queries.SocialAuth, graphene.ObjectType):
    hello_auth = graphene.String()
