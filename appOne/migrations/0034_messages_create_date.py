# Generated by Django 4.0 on 2023-08-05 15:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0033_alter_messages_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
