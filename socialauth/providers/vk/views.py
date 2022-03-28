from .provider import VKProvider
from ..views import OAuth2CallbackView

Callback_view = OAuth2CallbackView.from_provider(VKProvider)
