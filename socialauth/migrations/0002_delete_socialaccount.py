# Generated by Django 4.0.2 on 2022-04-25 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("socialauth", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SocialAccount",
        ),
    ]
