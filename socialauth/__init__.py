"""SocialProviders
Socialauth entry point. Prepare for work
Here we're read SOCIALAUTH__PROVIDERS, loads service registry
and generate SocialProviders enum
"""
from .providers import registry, ProvidersEnum

__all__ = ["registry", "SocialProviders"]

registry.load()
SocialProviders = ProvidersEnum.from_registry()
