# Generated by Django 5.0.6 on 2024-07-16 12:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="content",
            new_name="description",
        ),
    ]
