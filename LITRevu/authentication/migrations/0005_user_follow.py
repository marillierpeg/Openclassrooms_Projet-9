# Generated by Django 5.0.6 on 2024-07-25 14:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "authentication",
            "0004_alter_user_groups_alter_user_user_permissions_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="follow",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
