# Generated by Django 4.0 on 2023-07-24 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0022_alter_comments_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='post',
            field=models.CharField(max_length=5000000, null=True),
        ),
    ]
