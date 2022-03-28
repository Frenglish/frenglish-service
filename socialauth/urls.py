from django.urls import path, include
from .apps import SocialauthConfig

_app_name = SocialauthConfig.name

urlpatterns = [path("provider/", include("{}.providers.urls".format(_app_name)))]
