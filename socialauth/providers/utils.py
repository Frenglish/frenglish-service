from importlib import import_module
from django.conf import settings
from django.apps import apps
from django.http.request import HttpRequest

from ..apps import SocialauthConfig
from .oauth2 import OAuth2ProviderAbstract


def build_provider_url(request, provider):
    """
    :type request: HttpRequest
    :type provider: str
    :rtype: str
    """
    from ..apps import SocialauthConfig

    return request.build_absolute_uri(
        f"/{SocialauthConfig.name.lower()}/provider/{provider}"
    )


def get_app_config():
    return apps.get_app_config(SocialauthConfig.name)


def get_config(key):
    """
    :param key: Config key
    :type key: str
    :return: Config value from settings.py
    :rtype: any
    """
    app_named_prefix = SocialauthConfig.name.upper()
    return getattr(settings, "{}_{}".format(app_named_prefix, key.upper()), None)


def get_socialauth_providers_list():
    return get_config("providers")


def get_socialauth_providers():
    """
    :rtype: list[tuple[type[OAuth2ProviderAbstract], Any]]
    """
    settings_providers = get_config("providers")

    if settings_providers is None:
        raise RuntimeError(
            "Socialauth expected at least 1 registered provider that provides at least 1 service"
        )

    providers = []

    for provider_name in settings_providers:
        try:
            provider_module = import_module("{}.provider".format(provider_name))
        except ImportError:
            pass
        else:
            provider_class = getattr(provider_module, "provider", None)
            if provider_class is not None:
                provider_config = settings_providers.get(provider_name, None)
                pack = (provider_class, provider_config)
                providers.append(pack)

    return providers
