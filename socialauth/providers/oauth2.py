from abc import ABC, abstractmethod

from django.http import HttpRequest
from requests_oauthlib import OAuth2Session
from .account import UserData


class ProviderAbstract(ABC):
    id = None
    name = None
    provider_module_name = None

    _config = None

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
        :rtype: Dict[str, Any]
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
    :type adapter_class: type[OAuth2AdapterAbstract]
    """

    adapter_class = None

    def __init__(self, registry, **kwargs):
        super().__init__(**kwargs)

        if self.adapter_class is None or not issubclass(
            self.adapter_class, OAuth2AdapterAbstract
        ):
            raise AttributeError(
                f"You must specify `adapter` property as subclass of {OAuth2AdapterAbstract} "
                f"in {self.__class__}"
            )

        self._registry = registry

    @property
    def registry(self):
        """
        :return: Provider registry
        :rtype: Registry
        """
        return self._registry

    @abstractmethod
    def get_adapter(self, request):
        """
        :param request: Django request
        :type request: HttpRequest
        :return: An Adapter instance
        :rtype: OAuth2AdapterAbstract
        """
        raise NotImplementedError


class OAuth2Provider(OAuth2ProviderAbstract):
    def get_adapter(self, request):
        if not isinstance(request, HttpRequest):
            raise ValueError(
                f"`request` argument must be an instance of {HttpRequest.__name__}"
            )

        return self.adapter_class(request, provider=self)


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


class OAuth2AdapterAbstract(AdapterAbstract):
    auth_url = None
    access_token_url = None
    user_url = None
    scope = None

    def __init__(self, request, provider):
        super().__init__(request, provider)

        from socialauth.providers.utils import build_provider_url

        redirect_uri = f"{build_provider_url(request, provider=provider.id)}/callback"
        self._oauth2_session = OAuth2Session(
            client_id=provider.config.get("client_id"),
            redirect_uri=redirect_uri,
            scope=self.scope,
        )

    @property
    def session(self):
        """
        :rtype: OAuth2Session
        """
        return self._oauth2_session

    @abstractmethod
    def authorization_url(self, **kwargs):
        """
        :return: Tuple(url, state)
        :rtype: tuple[str, str]
        """
        return self.session.authorization_url(self.auth_url, **kwargs)

    @abstractmethod
    def fetch_token(self, code=None):
        raise NotImplementedError

    @abstractmethod
    def fetch_user_data(self, token=None):
        """
        :param token: str
        :rtype: UserData
        """
        raise NotImplementedError


class OAuth2Adapter(OAuth2AdapterAbstract):
    def authorization_url(self):
        return self.session.authorization_url(self.auth_url)

    def fetch_token(self, code=None):
        client_secret = self.provider.config.get("client_secret")
        code = code or self.request.GET.get("code")

        return self.session.fetch_token(
            self.access_token_url,
            client_secret=client_secret,
            code=code,
            include_client_id=True,
        )

    def fetch_user_data(self, token=None):
        response = self.session.get(self.user_url)

        from json import loads

        data = loads(response.text)

        return UserData(
            id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
        )
