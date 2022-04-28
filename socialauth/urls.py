from django.urls import re_path, path, include
from .providers import urls

__all__ = ["create_urls", "urlpatterns"]


def create_urls():
    from .config import SocialauthConfig

    return re_path(f"{SocialauthConfig.root_path}/", include("socialauth.urls"))


urlpatterns = [path("provider/", include(urls))]
