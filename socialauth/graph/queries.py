import graphene

from .types import SocialProvidersEnum
from ..providers import registry


class SocialAuth(graphene.ObjectType):
    social_auth_services = graphene.List(graphene.String)
    get_socialauth_url = graphene.String(
        provider=SocialProvidersEnum(), forward=graphene.String()
    )
    get_token = graphene.String()

    def resolve_get_token(root, info):
        from graphql_jwt.shortcuts import get_token

        get_token(info.context.user)
        return ""

    def resolve_social_auth_services(root, info):
        return registry.get_names()

    def resolve_get_socialauth_url(root, info, provider, forward):
        provider = registry.get_provider(provider)
        adapter = provider.get_adapter(info.context)
        url, _ = adapter.authorization_url()
        return url
