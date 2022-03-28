from enum import Enum

from .utils import get_socialauth_providers
from ..base import Singleton

from .oauth2 import OAuth2ProviderAbstract


class Registry(metaclass=Singleton):
    _providers = None
    loaded = None

    def __init__(self):
        self._providers = {}
        self.loaded = False

    def get_names(self):
        return list(self._providers.keys())

    def get_providers_list(self):
        return list(self._providers.values())

    def get_provider(self, provider):
        """
        :param provider: Provider id or class
        :type provider: type[OAuth2ProviderAbstract] or str or Enum
        :return: Provider instance
        :rtype: OAuth2ProviderAbstract
        """
        if isinstance(provider, Enum):
            provider = provider.name.lower()
        elif issubclass(provider, OAuth2ProviderAbstract):
            provider = provider.id

        if provider not in self._providers:
            raise ValueError(f"Provider `{provider}` are not registered")

        return self._providers[provider]

    def register(self, provider: OAuth2ProviderAbstract) -> None:
        name = provider.id
        if hasattr(self._providers, name):
            raise NameError(
                "Registry, duplicate key error, provider `{}` already registered".format(
                    name
                )
            )

        self._providers[name] = provider

    def load(self):
        if self.loaded is True:
            return

        providers = get_socialauth_providers()

        for provider in providers:
            provider_class, provider_config = provider
            provider_instance = provider_class(self, **provider_config)
            self.register(provider_instance)

        self.loaded = True


class ProvidersEnum(Enum):
    @classmethod
    def from_registry(cls):
        """
        Lookup registry for loaded services and builds Enum using service name as key and value

        :return: Enumerate of registered services
        :rtype: ProvidersEnum
        :raises RuntimeError: If service registry not loaded yet
        """
        if not registry.loaded:
            raise RuntimeError(
                "Service registry are not loaded yet."
                "\n- Maybe you trying init ProviderEnum before Django loads socialauth app."
                "\n- Check for 'socialauth' specified in INSTALLED_APPS."
            )

        services = [name_upper.upper() for name_upper in registry.get_names()]
        services_dict = dict(zip(services, services))
        return cls(cls.__name__, services_dict)


registry = Registry()
