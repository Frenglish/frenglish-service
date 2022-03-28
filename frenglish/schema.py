import graphene
import socialauth.graph.schema


class Query(socialauth.graph.schema.Query, graphene.ObjectType):
    pass


class Mutations(socialauth.graph.schema.Mutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
