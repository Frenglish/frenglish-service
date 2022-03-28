from django.views.generic import View

from frenglish.core.response import create_response

from .oauth2 import OAuth2ProviderAbstract


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
        adapter = self.provider.get_adapter(request)

        if "code" not in request.GET:
            return create_response(error="authorization code required")

        return create_response(
            adapter.obtain_access_token_by_code(request.GET.get("code"))
        )
