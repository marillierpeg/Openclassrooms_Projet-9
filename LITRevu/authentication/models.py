from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    username = models.CharField("username", max_length=50, unique=True,  error_messages={
        'unique': ("Ce nom d'utilisateur est déjà attribué")
        }
    )
    email = models.EmailField("Email", unique=True, )
    password = models.CharField("mot de passe", max_length=50, )
    profile_photo = models.ImageField(
        verbose_name="photo de profil", default="static/default_profile.png",
        upload_to="profile_photos/"
    )
    is_online = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    groups = models.ManyToManyField(Group, related_name="user_auth_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="user_auth_permissions")
