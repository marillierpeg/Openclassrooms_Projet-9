from authentication.models import User
from .models import Review, Post, UserFollows
from .forms import ReviewForm, PostForm, FollowedUserForm, PostReviewForm

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View


class ViewReview(View, LoginRequiredMixin):

    def review_and_photo_upload(request):
        review_form = ReviewForm()
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.author = request.user
                review.save()
                return redirect("home")
        context = {
            "review_form": review_form,
        }
        return render(request, "reviews/create_review.html", context=context)

    def view_review(request, review_id):
        review = get_object_or_404(Review, id=review_id)
        return render(request, "reviews/view_review.html", {"review": review})

    def update_review(request, review_id):
        review = get_object_or_404(Review, id=review_id)
        edit_review = ReviewForm(instance=review)
        if request.method == "POST":
            edit_review = ReviewForm(request.POST, request.FILES, instance=review)
            if edit_review.is_valid():
                edit_review.save()
            return redirect("view_review", review.id)
        context = {"edit_review": edit_review}
        return render(request, "reviews/update_review.html", context=context)

    def delete_review(request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.method == "POST":
            review.delete()
            return redirect("home")
        return render(request, "reviews/delete_review.html", {"review": review})


class ViewPostReview(View, LoginRequiredMixin):

    def answer_post(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.method == "POST":
            form = PostReviewForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                # Vérifie si l'utilisateur à déjà créer une review sur un post
                if not Review.objects.filter(author=request.user, post=post).exists():
                    review = form.save(commit=False)
                    review.author = request.user
                    review.post = post
                    review.save()
                    return redirect("home")
                else:
                    messages.error(request, "Une review a déjà été publiée en réponse à ce post")
        else:
            form = PostReviewForm()
        context = {"post_review_form": form, "post": post}
        return render(request, "reviews/create_review_post.html", context=context)


class ViewPost(View, LoginRequiredMixin):

    def post_upload(request):
        post_form = PostForm()
        if request.method == "POST":
            post_form = PostForm(request.POST)
            if (post_form.is_valid()):
                post = post_form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect("home")
        context = {"post_form": post_form}
        return render(request, "reviews/create_post.html", context=context)

    def view_post(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        return render(request, "reviews/view_post.html", {"post": post})

    def update_post(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        edit_post = PostForm(instance=post)
        if request.method == "POST":
            edit_post = PostForm(request.POST, instance=post)
            if edit_post.is_valid():
                edit_post.save()
                return redirect("view_post", post.id)
        context = {"edit_post": edit_post}
        return render(request, "reviews/update_post.html", context=context)

    def delete_post(request, post_id):
        post = Post.objects.get(id=post_id)
        if request.method == "POST":
            post.delete()
            return redirect("home")
        return render(request, "reviews/delete_post.html", {"post": post})


class ViewHome(View, LoginRequiredMixin):

    def home(request):
        reviews = Review.objects.all()
        posts = Post.objects.all()
        following = UserFollows.objects.all()
        return render(
            request, "reviews/home.html", context={"reviews": reviews, "posts": posts, "follows": following})


class FollowingView(LoginRequiredMixin, View):
    """Cette vue gère l'affichage et la gestion des utilisateurs suivis par l'utilisateur connecté."""
    def display_follows(request):
        """Affiche les utilisateurs déjà suivis."""
        # Récupérer les utilisateurs que vous suivez
        followed_users = UserFollows.objects.filter(user=request.user)

        # Récupérer les utilisateurs qui vous suivent
        users_following = UserFollows.objects.filter(followed_user=request.user)

        form = FollowedUserForm()

        context = {
            "form": form,
            "followed_users": followed_users,
            "users_following": users_following,
        }
        return render(request, "reviews/followed_users.html", context=context)

    def follow_users(request):
        """ Traite le formulaire pour suivre de nouveaux utilisateurs."""
        form = FollowedUserForm(request.POST)
        followed_users = UserFollows.objects.filter(user=request.user)

        if form.is_valid():
            follows_username = form.cleaned_data["follows"]
            try:
                followed_user = User.objects.get(username=follows_username)
                if followed_user != request.user:
                    # Enregistrer la relation de suivi dans un seul sens
                    UserFollows.objects.get_or_create(user=request.user, followed_user=followed_user)
                    return redirect("followed_users")
                else:
                    messages.error(request, "Vous ne pouvez pas vous abonner à vous-même.")
            except User.DoesNotExist:
                messages.error(request, "Utilisateur inconnu.")

        context = {
            "form": form,
            "followed_users": followed_users
        }
        return render(request, "reviews/follow_users.html", context=context)
