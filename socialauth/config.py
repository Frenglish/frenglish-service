import enum
from dataclasses import dataclass

from django.conf import settings

from socialauth.apps import SocialauthConfig as SocialAuthDjangoConfig


def get_config(key, fallback=None):
    """
    :param fallback: Default parameter if config does dot exist
    :type fallback: any
    :param key: Config key
    :type key: str or enum.Enum
    :return: Config value from settings.py
    :rtype: any
    """
    if isinstance(key, enum.Enum):
        key = key.name

    app_named_prefix = SocialAuthDjangoConfig.name.upper()
    return getattr(settings, "{}_{}".format(app_named_prefix, key.upper()), fallback)


class SocialAuthConfigEnum(enum.Enum):
    ROOT_PATH = "ROOT_PATH", SocialAuthDjangoConfig.name


@dataclass
class SocialauthConfig:
    """
    Socialauth config with defaults
    """

    root_path = get_config(SocialAuthConfigEnum.ROOT_PATH, SocialAuthDjangoConfig.name)
