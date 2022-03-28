from django.urls import path

from .views import Callback_view

urlpatterns = [path("callback", Callback_view)]
