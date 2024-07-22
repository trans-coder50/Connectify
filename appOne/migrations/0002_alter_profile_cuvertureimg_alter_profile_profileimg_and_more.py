# Generated by Django 4.0 on 2023-07-19 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cuvertureImg',
            field=models.ImageField(default='film25.jpg', upload_to='img'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profileImg',
            field=models.ImageField(default='film25.jpg', upload_to='img'),
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postImg', models.ImageField(upload_to='img')),
                ('content', models.CharField(max_length=200, null=True)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appOne.profile')),
            ],
        ),
    ]