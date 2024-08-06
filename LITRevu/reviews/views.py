from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from .models import Review, Post
from .forms import ReviewForm, PostForm, FollowedUserForm


@login_required
class ViewReview(View):

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


@login_required
class ViewPost(View):

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


@login_required
class ViewHome(View):

    def home(request):
        reviews = Review.objects.all()
        posts = Post.objects.all()
        return render(
            request, "reviews/home.html", context={"reviews": reviews, "posts": posts})


@login_required
class ViewFollowedUser(View):

    def follow_users(request):
        form = FollowedUserForm(instance=request.user)
        if request.method == "POST":
            form = FollowedUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("home")
        return render(request, "reviews/follow_users.html", context={"form": form})
