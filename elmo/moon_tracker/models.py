from django.db import models, IntegrityError
from django.conf import settings

from eve_sde.models import Moon as SDEMoon


def get_ore_name_from_id(oid):
    r = []

    for x in ORE_CHOICES:
        r += x[1]

    return dict(r)[oid]


class Moon(SDEMoon):
    def get_annotation(self):
        return MoonAnnotation.objects.get_or_create(
            moon=self,
            defaults={
                'alert': False,
                'final_scan': None
            }
        )

    def add_scan(self, owner, materials):
        try:
            result = ScanResult.objects.create(
                moon=self,
                owner=owner
            )
        except IntegrityError:
            raise ScanResult.AlreadyExistsError

        for ore, quantity in materials.items():
            ScanResultOre.objects.create(
                scan=result,
                ore_id=ore,
                quantity=quantity
            )

        self.attempt_finalization()

    def attempt_finalization(self):
        print(self)

    class Meta:
        proxy = True


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

    class AlreadyExistsError(Exception):
        pass


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


class MoonAnnotation(models.Model):
    moon = models.OneToOneField(Moon, primary_key=True)
    alert = models.BooleanField(db_index=True)
    final_scan = models.ForeignKey(ScanResult, null=True)
