from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )


class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_photo', )
