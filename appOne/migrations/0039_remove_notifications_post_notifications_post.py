# Generated by Django 4.0 on 2023-08-06 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0038_notifications_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='Post',
        ),
        migrations.AddField(
            model_name='notifications',
            name='post',
            field=models.IntegerField(null=True),
        ),
    ]
