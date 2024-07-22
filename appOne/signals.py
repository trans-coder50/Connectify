
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import delete_expired_item
from .models import *

@receiver(post_save, sender=Stories)
def schedule_deletion(sender, instance, **kwargs):
    delete_expired_item.apply_async((instance.id,), countdown=60*60*24) 

@receiver(post_save, sender=Hearts)
def reaction(sender, instance, **kwargs):
    print(instance)
    user = instance.username
    post = instance.post
    Notifications.objects.create(user=user,post=post,notification= "has reacted to your post")
@receiver(post_save, sender=Comments)
def commenting(sender, instance, **kwargs):
    print(instance)
    user = instance.username
    post = instance.post
    Notifications.objects.create(user=user,post=post,notification= "has commented to your post")