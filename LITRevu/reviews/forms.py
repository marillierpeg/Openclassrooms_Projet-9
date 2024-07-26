from django import forms
from . import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ["image", "caption"]


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

    class Meta:
        model = models.Review
        fields = ["title", "description", "rating"]


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
