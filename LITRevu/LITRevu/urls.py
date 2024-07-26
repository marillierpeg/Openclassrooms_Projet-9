from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.conf import settings
from django.conf.urls.static import static
import reviews.views
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
    path("reviews/create_review/", reviews.views.review_and_photo_upload, name="create_review"),
    path("reviews/create_post/", reviews.views.post_upload, name="create_post"),
    path("reviews/view_review/<int:review_id>/", reviews.views.view_review, name="view_review"),
    path("reviews/view_post/<int:post_id>/", reviews.views.view_post, name="view_post"),
    path("reviews/update_review/<int:review_id>/", reviews.views.update_review, name="update_review"),
    path("reviews/update_post/<int:post_id>/", reviews.views.update_post, name="update_post"),
    path("reviews/delete_review/<int:review_id>/", reviews.views.delete_review, name="delete_review"),
    path("reviews/delete_post/<int:post_id>/", reviews.views.delete_post, name="delete_post"),
    path("home/", reviews.views.home, name="home"),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
# les images sont stockées en local (environnement de dev pas en production)
# On fournit un chemin qui pointe vers le serveur local
