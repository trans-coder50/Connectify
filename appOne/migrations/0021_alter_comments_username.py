# Generated by Django 4.0 on 2023-07-21 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('appOne', '0020_alter_comments_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
    ]
