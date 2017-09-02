from django.db import models
from django.conf import settings

from eve_sde.models import Moon, Ore

# Create your models here.
class ScanResult(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='scans',
        db_index=True
    )

    moon = models.ForeignKey(
        Moon,
        related_name='scans',
        db_index=True
    )

class ScanResultOre(models.Model):
    scan = models.ForeignKey(
        ScanResult,
        related_name='constituents',
        db_index=True
    )

    ore = models.ForeignKey(
        Ore,
        related_name='+'
    )

    percentage = models.PositiveSmallIntegerField()
