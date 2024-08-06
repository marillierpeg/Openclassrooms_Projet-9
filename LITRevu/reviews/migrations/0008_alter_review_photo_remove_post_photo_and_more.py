# Generated by Django 5.0.6 on 2024-08-05 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_photo_image_alter_review_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='photo',
            field=models.ImageField(blank=True, default='static/no-image.jpg', null=True, upload_to='static/'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='photo',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='author',
            new_name='user',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
