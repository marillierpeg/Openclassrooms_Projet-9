# from authentication.models import User
from .models import Review, Post, UsersFollowing
from .forms import ReviewForm, PostForm, FollowedUserForm

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from authentication.models import User


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

    def get_post_review(request, post_id):
        post= get_object_or_404(Post, id=post_id)
        post_review_form = ReviewForm(instance=post)
        if request.method == "POST":
            post_review_form = ReviewForm(request.POST, request.FILES, instance=post)
            if post_review_form.is_valid():

                review = post_review_form.save()
                review.author = request.user
                review.post = post
                review.save()
                return redirect("home")
        else:
            post_review_form = ReviewForm()
        context = {"post_review_form": post_review_form, "post_review": post}
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


class ViewFollowing(LoginRequiredMixin, View):

    def follow_users(request):
        """ Gère le formulaire pour suivre de nouveaux utilisateurs."""
        form = FollowedUserForm(request.POST)
        followed_users = UsersFollowing.objects.filter(user=request.user)
        if form.is_valid():
            # Récupérer les utilisateurs sélectionnés dans le formulaire
            selected_users = form.cleaned_data['follows']
            try:
                followed_users = User.objects.get(username=selected_users)
                if followed_users != request.user:
                    UsersFollowing.objects.get_or_create(user=request.user, followers=followed_users)
                    return redirect("followed_users")
                else:
                    messages.error(request, "Vous ne pouvez pas vous abonner à votre propre compte")
            except User.DoesNotExist:
                # Gérer le cas où l'utilisateur sélectionné n'existe pas
                messages.error(request, "Cet utilisateur n'existe pas.")
        context = {
            "form": form,
            "followed_users": followed_users
        }
        return render(request, "reviews/follow_users.html", context=context)

    def display_followers(request):
        """Affiche les utilisateurs suivis"""
        # Récupérer les utilisateurs que vous suivez
        followed_users = UsersFollowing.objects.filter(user=request.user)

        # Récupérer les utilisateurs qui vous suivent
        users_following = UsersFollowing.objects.filter(followers=request.user)

        form = FollowedUserForm()

        context = {
            "form": form,
            "followed_users": followed_users,
            "users_following": users_following,
        }
        return render(request, "reviews/followed_users.html", context=context)


class ViewUnfollow(LoginRequiredMixin, View):

    def post(self, request):
        user_to_unfollow_id = request.POST.get('followers_id')
        try:
            follow = UsersFollowing.objects.get(user=request.user, followers_id=user_to_unfollow_id)
            follow.delete()
            messages.success(request, "Vous ne suivez plus cet utilisateur.!!!!!!!!!!!!!!!!!!!!!!")
        except UsersFollowing.DoesNotExist:
            messages.error(request, "L'abonnement n'existe pas.§§§§§§§§§§§§§§§§§§§§§§§§§§")
        except Exception:
            messages.error(request, "Une erreur inattendue s'est produite. Veuillez réessayer plus tard.")
        return redirect('followed_users')


class ViewHome(LoginRequiredMixin, View):

    def home(request):

        followed = UsersFollowing.objects.filter(user=request.user)
        followed_users_ids = followed.values_list("followers_id", flat=True)
        reviews = Review.objects.filter(author__in=followed_users_ids)
        posts = Post.objects.all()
        return render(
            request, "reviews/home.html", context={"reviews": reviews, "posts": posts}
        )
