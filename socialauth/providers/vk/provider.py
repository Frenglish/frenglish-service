from ..oauth2 import OAuth2Provider, OAuth2Adapter


EXTRACT_FIELDS = ["id", "first_name", "last_name", "crop_photo", "domain"]


class VKScope:
    EMAIL = 1 << 22
    NOTIFY = 1 << 0
    FRIENDS = 1 << 1
    PHOTOS = 1 << 2
    AUDIO = 1 << 3
    VIDEO = 1 << 4
    STORIES = 1 << 6
    PAGES = 1 << 7
    STATUS = 1 << 10
    NOTES = 1 << 11
    OFFLINE = 1 << 16
    DOCS = 1 << 17
    NOTIFICATIONS = 1 << 19
    STATS = 1 << 20
    MARKET = 1 << 27

    @staticmethod
    def build_scope(*scopes):
        scope = 0
        for s in scopes:
            scope |= s
        return str(scope)


class VKAdapter(OAuth2Adapter):
    auth_url = "https://oauth.vk.com/authorize"
    access_token_url = "https://oauth.vk.com/access_token"
    user_url = "https://api.vk.com/method/users.get"
    scope = VKScope.build_scope(VKScope.EMAIL)

    def authorization_url(self):
        return self.session.authorization_url(
            self.auth_url,
            v=self.provider.config.get("api_version", "5.131"),
        )

    def fetch_user_data(self, token=None):
        url_params = {
            "v": self.provider.config.get("api_version", "5.131"),
            "client_id": self.provider.config.get("client_id"),
            "fields": ",".join(EXTRACT_FIELDS),
        }

        response = self.session.get(self.user_url, params=url_params)

        from ..account import UserData

        data = response.json().get("response", [])[0]

        return UserData(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=self.session.token.get("email"),
            username=data.get("domain"),
        )


class VKProvider(OAuth2Provider):
    id = "vk"
    name = "VK"
    adapter_class = VKAdapter


provider = VKProvider
