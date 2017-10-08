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
        (18, 'Plagioclase'),
        (19, 'Spodumain'),
        (20, 'Kernite'),
        (21, 'Hedbergite'),
        (22, 'Arkonor'),
        (1223, 'Bistot'),
        (1224, 'Pyroxeres'),
        (1225, 'Crokite'),
        (1226, 'Jaspet'),
        (1227, 'Omber'),
        (1228, 'Scordite'),
        (1229, 'Gneiss'),
        (1230, 'Veldspar'),
        (1231, 'Hemorphite'),
        (1232, 'Dark Ochre'),
        (11396, 'Mercoxit'),
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

    quantity = models.FloatField()

    class Meta:
        default_permissions = ()
