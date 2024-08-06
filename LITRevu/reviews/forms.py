from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from . import models


class ReviewForm(forms.ModelForm):
    title = forms.CharField(label="Titre de la critique", widget=forms.TextInput(
        attrs={"id": "title", "placeholder": "Titre de la critique"}
        ), required=True, error_messages={"required": "Veuillez saisir un titre."})
    rating = forms.IntegerField(
        label="Note /5",
        required=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = forms.CharField(label="Commentaire", widget=forms.Textarea(
        attrs={"id": "description", "placeholder": "Votre commentaire"}
        ), required=True, error_messages={"required": "Veuillez saisir une description."})

    photo = forms.ImageField(label="Image", required=False)
    image_description = forms.CharField(
        label="Description de l'image", required=False
    )

    class Meta:
        model = models.Review
        fields = ["title", "description", "rating", "photo"]


class PostForm(forms.ModelForm):
    title = forms.CharField(label="Titre de la demande", widget=forms.TextInput(
        attrs={"id": "title"}
        ), required=True, error_messages={"required": "Veuillez saisir un titre."})
    description = forms.CharField(
        label="Description", required=True, error_messages={
            "required": "Merci de préciser votre demande"
        }
    )

    class Meta:
        model = models.Post
        fields = ["title", "description"]


class FollowedUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["follow"]
