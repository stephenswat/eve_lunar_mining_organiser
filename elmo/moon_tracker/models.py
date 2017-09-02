from django.db import models
from django.conf import settings
from django.forms import Select

from eve_sde.models import Moon

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


ORE_CHOICES = (
    ('Standard Ores', (
        (1, 'PH1'),
        (2, 'PH2'),
    )),
    ('Moon Ores', (
        (3, 'PH3'),
        (4, 'PH4'),
    )),
)

class ScanResultOre(models.Model):
    scan = models.ForeignKey(
        ScanResult,
        related_name='constituents',
        db_index=True
    )

    ore = models.IntegerField(choices=ORE_CHOICES)

    percentage = models.PositiveSmallIntegerField()
