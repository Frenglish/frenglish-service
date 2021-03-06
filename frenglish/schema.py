import graphene
import socialauth.graph.schema
import graphql_jwt


class Query(socialauth.graph.schema.Query, graphene.ObjectType):
    pass


class Mutations(socialauth.graph.schema.Mutations, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
