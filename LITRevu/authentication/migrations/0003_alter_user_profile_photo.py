# Generated by Django 5.0.6 on 2024-07-16 08:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_user_is_online_user_profile_photo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_photo",
            field=models.ImageField(
                default="static/default_profile.png",
                upload_to="",
                verbose_name="photo de profil",
            ),
        ),
    ]
