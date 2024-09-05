from .models import Review, Post, UsersFollowing, PostReview
from .forms import ReviewForm, PostForm, FollowedUserForm
from authentication.models import User

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, OuterRef, Subquery
from django.views import View
from django.core.paginator import Paginator


class ViewReview(LoginRequiredMixin, View):

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


class ViewPostReview(LoginRequiredMixin, View):

    def create_review_from_post(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        initial_data = {"post": post}
        review_form = ReviewForm(request.POST, request.FILES or None, initial=initial_data)
        if request.method == "POST" and review_form.is_valid():
            review = review_form.save(commit=False)
            review.post = post
            review.author = request.user
            review.save()
            return redirect("home")
        return render(
            request,
            template_name="reviews/create_post_review.html",
            context={
                "post": post,
                "review_form": review_form,
            }
        )

    def view_post_review(request, post_id):
        post = get_object_or_404(PostReview, id=post_id)
        review = get_object_or_404(PostReview, id=post_id)
        return render(request, "reviews/view_review_post.html", {"post": post, "review": review})


class ViewPost(LoginRequiredMixin, View):

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
            selected_users = form.cleaned_data["follows"]
            try:
                followed_users = User.objects.get(username=selected_users)
                if followed_users != request.user:
                    # Vérifier si l'utilisateur est déjà suivi
                    if UsersFollowing.objects.filter(user=request.user, followers=followed_users).exists():
                        messages.error(request, f"Vous suivez déjà {followed_users}.")
                    else:
                        UsersFollowing.objects.get_or_create(user=request.user, followers=followed_users)
                        messages.success(request, (f"Vous suivez maintenant {followed_users} ."))
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
        """Affiche les utilisateurs suivis et les followers"""
        # Récupérer les utilisateurs que vous suivez
        followed_users = UsersFollowing.objects.filter(user=request.user, is_blocked=False)

        # Récupérer les utilisateurs qui vous suivent
        users_following = UsersFollowing.objects.filter(followers=request.user)

        blocked_users = UsersFollowing.objects.filter(user=request.user, is_blocked=True).select_related("followers")

        form = FollowedUserForm()

        context = {
            "form": form,
            "followed_users": followed_users,
            "users_following": users_following,
            "blocked_users": blocked_users,
        }
        return render(request, "reviews/followed_users.html", context=context)


class ViewUnfollow(LoginRequiredMixin, View):

    def post(self, request):
        user_to_unfollow_id = request.POST.get("followers_id")
        try:
            follow = UsersFollowing.objects.get(user=request.user, followers_id=user_to_unfollow_id)
            user_to_unfollow = User.objects.get(id=user_to_unfollow_id)
            follow.delete()
            messages.success(request, (f"Vous ne suivez plus {user_to_unfollow.username}."))
        except UsersFollowing.DoesNotExist:
            messages.error(request, "L'abonnement n'existe pas.")
        except Exception:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer plus tard.")
        return redirect("followed_users")


class ViewBlockUser(LoginRequiredMixin, View):

    def post(self, request):
        user_to_block_id = request.POST.get("user_to_block_id")
        try:
            user_to_block = User.objects.get(id=user_to_block_id)

            # Vérifier si l'utilisateur est déjà bloqué
            if UsersFollowing.objects.filter(user=request.user, followers=user_to_block, is_blocked=True).exists():
                messages.error(request, f"Vous avez déjà bloqué {user_to_block.username}.")
            else:
                # Créer ou mettre à jour l'entrée UsersFollowing
                following_instance, created = UsersFollowing.objects.get_or_create(
                    user=request.user,
                    followers=user_to_block,
                    defaults={'is_blocked': True}
                )
                if not created:
                    following_instance.is_blocked = True
                    following_instance.save()
                messages.success(request, f"Vous avez bloqué {user_to_block.username}.")
        except User.DoesNotExist:
            messages.error(request, "Cet utilisateur n'existe pas.")
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {e}")
        return redirect("followed_users")

    def block_users(self, request):
        blocked_users = UsersFollowing.objects.filter(user=request.user, is_blocked=True).select_related("followers")
        return render(request, 'reviews/followed_users.html', {'blocked_users': blocked_users})


class ViewUnblockUser(LoginRequiredMixin, View):

    def post(self, request):
        user_to_unblock_id = request.POST.get("user_to_unblock_id")
        try:
            # Récupérer l'instance UsersFollowing pour cet utilisateur
            follow_instance = UsersFollowing.objects.get(
                user=request.user, followers_id=user_to_unblock_id, is_blocked=True
            )

            # Débloquer l'utilisateur
            follow_instance.is_blocked = False
            follow_instance.save()

            messages.success(request, f"Vous avez débloqué {follow_instance.followers.username}.")
        except UsersFollowing.DoesNotExist:
            messages.error(request, "Cet utilisateur n'est pas bloqué.")
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {e}")
        return redirect("followed_users")


class ViewHome(LoginRequiredMixin, View):

    def home(request):

        followed = UsersFollowing.objects.filter(user=request.user, is_blocked=False)
        followed_users_ids = followed.values_list("followers_id", flat=True)

        # affiche les reviews des personnes suivies uniquement
        reviews = Review.objects.filter(
            Q(author__in=followed_users_ids) | Q(author=request.user)
        ).order_by("-date_created")

        # affiche seulement les posts sans réponse
        posts = Post.objects.exclude(
            id__in=Subquery(
                Review.objects.filter(post__id=OuterRef("id")).values("post_id")
            )
        ).order_by("-date_created")
        paginator = Paginator(reviews, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request, "reviews/home.html", context={"page_obj": page_obj, "posts": posts}
        )
