# Generated by Django 5.0.6 on 2024-08-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0016_remove_post_review_review_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersfollowing",
            name="is_blocked",
            field=models.BooleanField(default=False),
        ),
    ]
