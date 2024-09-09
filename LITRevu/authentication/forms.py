from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


User = get_user_model()


class SignupForm(UserCreationForm):
    """Formulaire pour création d'un nouvel utilisateur"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )


class UploadProfilePhotoForm(forms.ModelForm):
    """Formulaire pour l'ajout/modification d'une photo de profil à un utilisateur"""
    class Meta:
        model = User
        fields = ('profile_photo', )
