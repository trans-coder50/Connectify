# Generated by Django 4.0 on 2024-03-24 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0040_alter_profile_cuvertureimg_alter_profile_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileImg',
            field=models.ImageField(default='pr.png', upload_to='img'),
        ),
    ]