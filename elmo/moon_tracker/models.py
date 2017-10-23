from django.db import models
from django.conf import settings

from eve_sde.models import Moon


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


def get_ore_name_from_id(oid):
    r = []

    for x in ORE_CHOICES:
        r += x[1]

    return dict(r)[oid]


class Mineral(models.Model):
    RARITY_CHOICES = (
        ('mineral', 'Mineral'),
        ('r4', 'R4'),
        ('r8', 'R8'),
        ('r16', 'R16'),
        ('r32', 'R32'),
        ('r64', 'R64'),
    )

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    rarity = models.CharField(choices=RARITY_CHOICES, max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()


class Ore(models.Model):
    RARITY_CHOICES = (
        ('standard', 'Standard'),
        ('ubiquitous', 'Ubiquitous'),
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('exceptional', 'Exceptional'),
    )

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    volume = models.FloatField()

    minerals = models.ManyToManyField(
        Mineral,
        through='OreMineral'
    )

    rarity = models.CharField(choices=RARITY_CHOICES, max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()


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

    ores = models.ManyToManyField(
        Ore,
        through='ScanResultOre'
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("owner", "moon"),)


class ScanResultOre(models.Model):
    scan = models.ForeignKey(ScanResult)
    ore = models.ForeignKey(Ore)
    quantity = models.FloatField()

    def get_percentage(self):
        return self.quantity * 100

    def get_moon(self):
        return self.scan.moon

    class Meta:
        default_permissions = ()


class OreMineral(models.Model):
    ore = models.ForeignKey(Ore)
    mineral = models.ForeignKey(Mineral)
    quantity = models.PositiveIntegerField()

    class Meta:
        default_permissions = ()
