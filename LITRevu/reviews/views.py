from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models


@login_required
def review_and_photo_upload(request):
    review_form = forms.ReviewForm()
    photo_form = forms.PhotoForm()
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([review_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            review = review_form.save(commit=False)
            review.author = request.user
            review.photo = photo
            review.save()
            return redirect("home")
    context = {
        "review_form": review_form,
        "photo_form": photo_form,
    }
    return render(request, "reviews/create_review.html", context=context)


@login_required
def post_upload(request):
    post_form = forms.PostForm()
    if request.method == "POST":
        post_form = forms.PostForm(request.POST)
        if (post_form.is_valid()):
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    context = {"post_form": post_form}
    return render(request, "reviews/create_post.html", context=context)


@login_required
def home(request):
    reviews = models.Review.objects.all()
    posts = models.Post.objects.all()
    return render(
        request, "reviews/home.html", context={"reviews": reviews, "posts": posts})


@login_required
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, "reviews/view_review.html", {"review": review})


@login_required
def view_post(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    return render(request, "reviews/view_post.html", {"post": post})


@login_required
def update_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_review = forms.ReviewForm(instance=review)
    if request.method == "POST":
        edit_review = forms.ReviewForm(request.POST, instance=review)
        if edit_review.is_valid():
            edit_review.save()
            return redirect("view_review", review.id)
    context = {"edit_review": edit_review}
    return render(request, "reviews/update_review.html", context=context)


@login_required
def update_post(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    edit_post = forms.PostForm(instance=post)
    if request.method == "POST":
        edit_post = forms.PostForm(request.POST, instance=post)
        if edit_post.is_valid():
            edit_post.save()
            return redirect("view_post", post.id)
    context = {"edit_post": edit_post}
    return render(request, "reviews/update_post.html", context=context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == "POST":
        review.delete()
        return redirect("home")
    return render(request, "reviews/delete_review.html", {"review": review})


@login_required
def delete_post(request, post_id):
    post = models.Post.objects.get(id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "reviews/delete_post.html", {"post": post})
