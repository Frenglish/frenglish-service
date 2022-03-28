import graphene
from graphql import GraphQLError

from . import types


class AuthMutation(graphene.Mutation):
    class Arguments:
        # provider = graphene.Argument(graphene.Enum.from_enum(Providers))
        code = graphene.String(required=True)

    access_token = graphene.String()

    @classmethod
    def mutate(cls, root, info, provider, code):
        try:
            return {"access_code": "adapter.auth_url"}
        except ModuleNotFoundError:
            raise GraphQLError("Invalid provider name: {}".format(provider))
