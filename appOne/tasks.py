from __future__ import absolute_import,unicode_literals
from celery import shared_task
from django.utils import timezone
from .models import Stories


@shared_task
def delete_expired_item(pk):
    print(pk)
    Stories.objects.get(id=pk).delete()
    print("deleted")