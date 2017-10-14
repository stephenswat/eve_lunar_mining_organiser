from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from eve_auth.models import EveUser


@receiver(post_save, sender=EveUser)
def my_handler(sender, **kwargs):
    if kwargs['instance'].character_id != 0 and kwargs['created']:
        Group.objects.get(name='default').user_set.add(kwargs['instance'])
