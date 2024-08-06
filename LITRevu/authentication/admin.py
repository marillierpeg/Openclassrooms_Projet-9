from django.contrib import admin
from authentication.models import User
from reviews.models import Post, Review


class PostAdmin(admin.TabularInline):
    """Interface en ligne pour l'administration des posts.
    Cette classe permet d'affiche et de gérer les posts
    dans le panneau d'administration Django."""
    model = Post


class ReviewAdmin(admin.TabularInline):
    """Interface en ligne pour l'administration des reviews.
    Cette classe permet d'afficher et de gérer les reviews
    dans le panneau d'administration Django."""
    model = Review


# class UserFollows(admin.TabularInline):
#     """Interface en ligne pour l'administration des suivis d'utilisateurs.
#     Cette classe fournit une interface en ligne pour l'administration des suivis d'utilisateurs.
#     Elle permet d'afficher et de gérer les relations de suivi entre les utilisateurs
#     dans le panneau d'administration Django."""
#     model = UserFollows


class UserAdmin(admin.ModelAdmin):
    """Interface d'administration pour le modèle User.
    Cette classe affiche les utilisateurs avec leurs attributs principaux
    Permet également de gérer les posts, les reviews et les suivis d'utilisateurs associés à chaque utilisateur."""
    inlines = [PostAdmin, ReviewAdmin]

    list_display = (
        "username",
        "is_superuser",
        "is_active",
        "date_joined",
    )


admin.site.register(User, UserAdmin)
