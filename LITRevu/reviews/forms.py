from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from . import models


User = get_user_model()


class ReviewForm(forms.ModelForm):
    """Formulaire pour la création d'une review"""
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
    """Formulaire pour la création d'un post"""
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


class PostReviewForm(forms.ModelForm):
    """Formulaire combiné pour la création d"un post et d"une review associée."""
    # Champs pour le post
    # post_title = forms.CharField(label="Titre", widget=forms.TextInput(
    #     attrs={"placeholder": "Titre du livre"}
    #     ), required=True, error_messages={"required": "Veuillez saisir un titre."})
    # description = forms.CharField(label="Description", widget=forms.TextInput
    #                               (attrs={"placeholder": "Description de la demande"}), required=True,
    #                               error_messages={"required": "Veuillez saisir une description."})
    # image = forms.ImageField(
    #     label="Image",
    #     required=False,
    #     widget=forms.ClearableFileInput(attrs={"aria-describedby": "image-help-text"}),
    #     help_text="Veuillez sélectionner une image.",
    # )
    # image_description = forms.CharField(
    #     label="Description de l'image", required=False, widget=forms.TextInput(
    #         attrs={"placeholder": "Description de l'image"}
    #     )
    # )

    # Champs pour la review
    review_title = forms.CharField(label="Titre de la review", widget=forms.TextInput(
        attrs={"id": "headline", "placeholder": "Titre de la review"}
        ), required=True, error_messages={"required": "Veuillez saisir un titre."}
    )
    photo = forms.ImageField(label="Image", required=False)
    image_description = forms.CharField(
        label="Description de l'image", required=False
    )
    rating = forms.IntegerField(
        label="Note",
        # widget=forms.HiddenInput(attrs={"id": "rating"}),
        required=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_description = forms.CharField(label="Commentaire", widget=forms.Textarea(
        attrs={"id": "body", "placeholder": "Votre commentaire"}
        ), required=True, error_messages={"required": "Veuillez saisir une description."})

    class Meta:
        model = models.PostReview
        fields = ["review_title", "rating", "photo", "review_description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FollowedUserForm(forms.ModelForm):
    """Formulaire pour suivre un utilisateur"""

    follows = forms.CharField(
        label="Utilisateurs à suivre", max_length=100, widget=forms.TextInput(
            attrs={"placeholder": "quel utilisateur voulez-vous suivre?"}
        ),
    )

    class Meta:
        model = User
        fields = ["follow"]

    def check_follows(self):
        """Vérifie si l'utilisateur à suivre existe."""
        follows = self.cleaned_data["follow"]

        if not User.objects.filter(username=follows):
            raise forms.ValidationError(
                "Utilisateur inconnu"
            )
        return follows
