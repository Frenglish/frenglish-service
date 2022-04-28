from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SocialAccount(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Related user"
    )
    provider = models.CharField(max_length=60, verbose_name="Socialauth provider name")
    uid = models.IntegerField(verbose_name="Social account user id")
    info = models.JSONField(verbose_name="Additional data of user social account")
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
