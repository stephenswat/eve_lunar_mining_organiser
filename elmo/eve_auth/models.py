from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from guardian.mixins import GuardianUserMixin

class EveUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, character_id, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)

        user = self.model(
            character_id=character_id,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.save(using=self._db)
        return user


class EveUser(AbstractBaseUser, PermissionsMixin):
    character_id = models.BigIntegerField(unique=True, db_index=True)

    is_staff = models.BooleanField(
        'Staff Status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )

    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = EveUserManager()

    USERNAME_FIELD = 'character_id'

    class Meta(object):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        abstract = False

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()
