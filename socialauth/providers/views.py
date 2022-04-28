from django.views.generic import View
from django.db.models import Model
from django.contrib.auth.models import AbstractBaseUser

from frenglish.core.response import create_response
from .oauth2 import OAuth2ProviderAbstract
from ..account.models import SocialAccount


def _connect_social_account(social_account, user):
    """
    :param social_account: SocialAccount model instance
    :type social_account: SocialAccount
    :param user: Any User model from `get_user_model()`
    :type user: AbstractBaseUser
    :return: True if connection success or False
    :rtype: bool
    """
    pass


class OAuth2CallbackView(View):
    """
    :param provider: OAuth2Provider instance
    :type provider: OAuth2ProviderAbstract
    """

    def __init__(self, provider, **kwargs):
        super().__init__(**kwargs)
        self.provider = provider

    @classmethod
    def from_provider(cls, provider_class, **factory_kwargs):
        """
        :type provider_class: type[OAuth2ProviderAbstract]
        """
        if not issubclass(provider_class, OAuth2ProviderAbstract):
            raise ValueError(
                f"`provider_class` must be subclass of `OAuth2ProviderAbstract`"
            )

        from . import registry

        def view(request, *args, **kwargs):
            provider = registry.get_provider(provider_class)

            self = cls(provider, **factory_kwargs)
            return self.dispatch(request, *args, **kwargs)

        return view

    def get(self, request):
        provider = self.provider
        adapter = provider.get_adapter(request)

        token = adapter.fetch_token()
        user_data = adapter.fetch_user_data(token)

        try:
            social_account = SocialAccount.objects.get(
                provider=provider.name,
                uid=user_data["id"],
            )
        except SocialAccount.DoesNotExist:
            from django.contrib.auth import get_user_model

            user_model = get_user_model()
            new_user = user_model(
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
            )

            if user_data.get("username"):
                new_user.username = user_data.get("username")

            new_user.set_unusable_password()
            new_user.save()

            social_account = SocialAccount(
                uid=user_data.get("id"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                provider=provider.name,
                info=user_data,
                user=new_user,
            ).save()

            _connect_social_account(social_account, new_user)

            return create_response({"USER": social_account["provider"]})
        else:
            return create_response({"USER": social_account.provider})
