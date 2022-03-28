import graphene

from .. import SocialProviders

SocialProvidersEnum = graphene.Enum.from_enum(SocialProviders)
