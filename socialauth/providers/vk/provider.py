from ..oauth2 import OAuth2ProviderAbstract, OAuth2Adapter


class VKAdapter(OAuth2Adapter):
    auth_url = "https://oauth.vk.com/authorize"
    access_token_url = "https://oauth.vk.com/access_token"
    user_url = "https://api.vk.com/method/users.get"


class VKProvider(OAuth2ProviderAbstract):
    id = "vk"
    name = "VK"
    adapter = VKAdapter

    def build_authorize_url(self, request):
        from urllib.parse import urlencode
        from ..utils import build_provider_url

        auth_url = self.adapter.auth_url
        redirect_uri = f"{build_provider_url(request, provider=self.id)}/callback"
        url_params = {
            "client_id": self.config.get("client_id"),
            "redirect_uri": redirect_uri,
            "v": self.config.get("api_version", "5.131"),
            "response_type": "code",
            "revoke": "1",
            "scope": 1 << 22,
        }
        return f"{auth_url}/?{urlencode(url_params)}"


provider = VKProvider
