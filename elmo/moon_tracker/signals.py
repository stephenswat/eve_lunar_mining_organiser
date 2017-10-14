from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from eve_auth.models import EveUser

DEFAULT_GROUP = Group.objects.get(name='default')

@receiver(post_save, sender=EveUser)
def my_handler(sender, **kwargs):
    if sender.character_id != 0 and kwargs['created']:
        DEFAULT_GROUP.user_set.add(kwargs['instance'])
