from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from django.conf import settings
from django.conf.urls.static import static
from reviews import views
import authentication.views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LoginView.as_view(
            template_name="authentication/login.html",
            redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("change-password/", PasswordChangeView.as_view(
        template_name="authentication/change_password.html"),
         name="password_change"
         ),
    path("change-password-done/", PasswordChangeDoneView.as_view(
        template_name="authentication/done_change_password.html"),
         name="password_change_done"
         ),
    path("profile-photo/upload/", authentication.views.upload_profile_photo,
         name="upload_profile_photo"),
    path("reviews/create_review/", views.ViewReview.review_and_photo_upload, name="create_review"),
    path("reviews/create_post/", views.ViewPost.post_upload, name="create_post"),
    path("reviews/view_review/<int:review_id>/", views.ViewReview.view_review, name="view_review"),
    path("reviews/view_post/<int:post_id>/", views.ViewPost.view_post, name="view_post"),
    path("reviews/update_review/<int:review_id>/", views.ViewReview.update_review, name="update_review"),
    path("reviews/update_post/<int:post_id>/", views.ViewPost.update_post, name="update_post"),
    path("reviews/delete_review/<int:review_id>/", views.ViewReview.delete_review, name="delete_review"),
    path("reviews/delete_post/<int:post_id>/", views.ViewPost.delete_post, name="delete_post"),
<<<<<<< HEAD
    path("reviews/create_review_post/<int:post_id>/", views.ViewPostReview.get_post_review, name="create_review_post"),
    path("follow_users/", views.ViewFollowing.follow_users, name="follow_users"),
    path("followed_users/", views.ViewFollowing.display_followers, name="followed_users"),
    path("unfollow/", views.ViewUnfollow.as_view(), name="unfollow_user"),
=======
    path("reviews/create_review_post/<int:post_id>/", views.ViewPostReview.answer_post, name="create_review_post"),
    path("follow_users/", views.FollowingView.follow_users, name="follow_users"),
    path("followed_users", views.FollowingView.display_follows, name="followed_users"),
>>>>>>> a46d6674188a9112ac89a533752d5f38ed7cd696
    path("home/", views.ViewHome.home, name="home"),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
# les images sont stockées en local (environnement de dev pas en production)
# On fournit un chemin qui pointe vers le serveur local
