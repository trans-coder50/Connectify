# Generated by Django 4.0 on 2023-07-19 15:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0009_remove_posts_createdat'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
