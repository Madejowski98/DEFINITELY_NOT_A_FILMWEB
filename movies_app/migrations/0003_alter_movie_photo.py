# Generated by Django 5.0.6 on 2024-05-31 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies_app", "0002_movie_approved_movie_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="media/"),
        ),
    ]
