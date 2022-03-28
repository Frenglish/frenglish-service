import graphene

from .types import SocialProvidersEnum
from ..providers import registry


class SocialAuth(graphene.ObjectType):
    social_auth_services = graphene.List(graphene.String)
    social_auth = graphene.String(provider=SocialProvidersEnum())

    def resolve_social_auth_services(root, info):
        return registry.get_names()

    def resolve_social_auth(root, info, provider):
        provider = registry.get_provider(provider)
        return provider.build_authorize_url(info.context)
