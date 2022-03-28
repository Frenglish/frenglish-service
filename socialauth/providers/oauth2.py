from abc import ABC, abstractmethod

from django.http import HttpRequest


class ProviderAbstract(ABC):
    id = None
    name = None
    provider_module_name = None

    _config = None
    _oauth_session = None

    def __init__(self, **kwargs):
        if "client_id" and "client_secret" not in kwargs:
            raise ValueError(
                f"Specify `client_id` and `client_secret` config for provider {self}"
            )

        self._config = {}
        for key, value in kwargs.items():
            self._config[key] = value

    @property
    def config(self):
        """
        :rtype: dict
        """
        return self._config

    def get_module_name(self):
        module_name = self.provider_module_name
        return (
            module_name
            if module_name is not None
            else self.__module__.rpartition(".")[0]
        )


class OAuth2ProviderAbstract(ProviderAbstract):
    """
    :type adapter: type[OAuth2AdapterAbstract]
    """

    adapter = None

    def __init__(self, registry, **kwargs):
        if self.adapter is None or not issubclass(self.adapter, OAuth2AdapterAbstract):
            raise AttributeError(
                f"You must specify `adapter` property as subclass of {OAuth2AdapterAbstract} "
                f"in {self.__class__}"
            )

        super().__init__(**kwargs)
        self._registry = registry

    @property
    def registry(self):
        """
        :return: Provider registry
        :rtype: Registry
        """
        return self._registry

    def get_adapter(self, request):
        """
        :param request: Django request
        :type request: HttpRequest
        :return: An Adapter instance
        :rtype: OAuth2AdapterAbstract
        """
        if not isinstance(request, HttpRequest):
            raise ValueError(
                f"`request` argument must be an instance of {HttpRequest.__name__}"
            )

        return self.adapter(request, provider=self)

    @abstractmethod
    def build_authorize_url(self, request):
        """
        :param request: Django request
        :type request: HttpRequest
        :rtype: str
        """
        raise NotImplementedError(f"build_authorize_url() in {self}")


# TODO: No adapters maybe?
class AdapterAbstract(ABC):
    def __init__(self, request, provider):
        if not isinstance(request, HttpRequest):
            raise ValueError(
                f"`request` argument must be an instance of {HttpRequest.__name__}"
            )
        if not isinstance(provider, ProviderAbstract):
            raise ValueError(
                f"`provider` argument must be an instance of {ProviderAbstract.__name__}"
            )

        self.request = request
        self.provider = provider


class OAuth2AdapterAbstract(AdapterAbstract, ABC):
    auth_url = None
    access_token_url = None
    user_url = None

    def __init__(self, request, provider):
        super().__init__(request, provider)

    @abstractmethod
    def obtain_access_token_by_code(self, code):
        raise NotImplementedError


class OAuth2Adapter(OAuth2AdapterAbstract):
    def obtain_access_token_by_code(self, code):
        pass
