from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    username = models.OneToOneField(User,null = True, on_delete = models.SET_NULL)
    profileImg = models.ImageField(upload_to="img", height_field=None, width_field=None,default="pr.png")
    cuvertureImg = models.ImageField(upload_to="img", height_field=None, width_field=None,default="grey.jfif")

    def __str__(self):
        return self.username.username
        
class Posts(models.Model):
    username = models.ForeignKey(User,null = True, on_delete = models.SET_NULL)
    postImg = models.ImageField(upload_to="img", height_field=None, width_field=None)
    content = models.CharField(max_length=200,null = True)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username.username

class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_friends')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_friends')

    def __str__(self):
        return f"{self.user1} - {self.user2}"

class Comments(models.Model):
    username = models.ForeignKey(User,null = True, on_delete = models.SET_NULL)
    comment = models.CharField(max_length=500,null = True)
    post = models.IntegerField(null = True)
    create_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.username.username

class Saves(models.Model):
    username = models.ForeignKey(User,null = True, on_delete = models.SET_NULL)
    post = models.IntegerField(null = True)
    def __str__(self):
        return self.username.username

class Hearts(models.Model):
    username = models.ForeignKey(User,null = True, on_delete = models.SET_NULL)
    post = models.IntegerField(null = True)
    def __str__(self):
        return self.username.username

class UserStatus(models.Model):
    user = models.OneToOneField(User,null = True, on_delete = models.SET_NULL)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Stories(models.Model):
    user =  models.OneToOneField(User,null = True, on_delete = models.SET_NULL)
    create_date = models.DateTimeField(default=timezone.now)
    story= models.ImageField(upload_to="img", height_field=None, width_field=None)
    def __str__(self):
        return self.user.username

class Rooms(models.Model):
    userOne=models.ForeignKey(User,null = True, on_delete = models.SET_NULL, related_name='user1')
    userTwo=models.ForeignKey(User,null = True, on_delete = models.SET_NULL,related_name='user2')
    def __str__(self):
        return f"{self.userOne} - {self.userTwo}"

class Messages(models.Model):
    user=models.ForeignKey(User,null = True, on_delete = models.SET_NULL)
    message=models.CharField(max_length=1000,null = True)
    room=models.ForeignKey(Rooms,null = True, on_delete = models.SET_NULL)
    create_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username

class Invitations(models.Model):
    sent_by=models.ForeignKey(User,null = True, on_delete = models.SET_NULL, related_name='sent_by')
    sent_to=models.ForeignKey(User,null = True, on_delete = models.SET_NULL,related_name='sent_to')
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sent_by} - {self.sent_to}"

class Notifications(models.Model):
    user=models.ForeignKey(User,null = True, on_delete = models.SET_NULL)
    post=models.IntegerField(null = True)
    notification = models.CharField(max_length=200,null = True)
    create_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username


