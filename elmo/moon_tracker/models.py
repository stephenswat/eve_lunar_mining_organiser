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

    class Meta:
        unique_together = (("owner", "moon"),)


ORE_CHOICES = (
    ('Standard Ores', (
        (46675, 'Dark Ochre'),
        (46676, 'Bistot'),
        (46677, 'Crokite'),
        (46678, 'Arkonor'),
        (46679, 'Gneiss'),
        (46680, 'Hedbergite'),
        (46681, 'Hemorphite'),
        (46682, 'Jaspet'),
        (46683, 'Kernite'),
        (46684, 'Omber'),
        (46685, 'Plagioclase'),
        (46686, 'Pyroxeres'),
        (46687, 'Scordite'),
        (46688, 'Spodumain'),
        (46689, 'Veldspar'),
    )),
    ('Moon Ores', (
        (45490, 'Zeolites'),
        (45491, 'Sylvites'),
        (45492, 'Bitumens'),
        (45493, 'Coesite'),

        (45494, 'Cobaltite'),
        (45495, 'Euxenite'),
        (45496, 'Titanite'),
        (45497, 'Scheelite'),

        (45498, 'Otavite'),
        (45499, 'Sperrylite'),
        (45500, 'Vanadinite'),
        (45501, 'Chromite'),

        (45502, 'Carnotite'),
        (45503, 'Zircon'),
        (45504, 'Pollucite'),
        (45506, 'Cinnabar'),

        (45510, 'Xenotime'),
        (45511, 'Monazite'),
        (45512, 'Loparite'),
        (45513, 'Ytterbite'),
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

    def get_percentage(self):
        return self.quantity * 100

    class Meta:
        default_permissions = ()
