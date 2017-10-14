from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from guardian.shortcuts import assign_perm

from eve_sde.models import Region


class Command(BaseCommand):
    help = 'Creates default permission groups.'

    def handle(self, *args, **options):
        self.create_default_group()
        self.create_admin_group()
        self.create_observer_group()

    def create_default_group(self):
        group, _ = Group.objects.get_or_create(name='default')

    def create_admin_group(self):
        group, _ = Group.objects.get_or_create(name='admin')

        for r in Region.objects.all():
            assign_perm('reg_can_view_scans', group, r)
            assign_perm('reg_can_add_scans', group, r)
            assign_perm('reg_can_delete_scans', group, r)

    def create_observer_group(self):
        group, _ = Group.objects.get_or_create(name='observer')

        for r in Region.objects.all():
            assign_perm('reg_can_view_scans', group, r)
