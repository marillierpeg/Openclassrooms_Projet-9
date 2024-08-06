from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to="books_covers/", default="static/no-image.png")
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.title

    IMAGE_MAX_SIZE = (200, 200)

    def resize_image(self):
        photo = Image.open(self.photo)
        photo.thumbnail(self.IMAGE_MAX_SIZE)
        photo.save(self.photo.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def checking_review(self, user):
        return Review.objects.filter(user=user, post_id=self.post_id).exists()
