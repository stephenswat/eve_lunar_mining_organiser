from django.db import models, IntegrityError
from django.conf import settings

from eve_sde.models import Moon as SDEMoon
import logging
import math


logger = logging.getLogger(__name__)


class Moon(SDEMoon):
    def get_annotation(self):
        ann, _ = MoonAnnotation.objects.get_or_create(
            moon=self,
            defaults={
                'alert': False,
                'final_scan': None
            }
        )

        return ann

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

        logger.info(
            "New scan for %s added by user %s.",
            str(self),
            owner.get_full_name()
        )

        self.attempt_finalization()

    def attempt_finalization(self):
        if self.scans.count() < settings.MOON_TRACKER_MINIMUM_SCANS:
            logger.info(
                "Finalization not started for %s: %d/%d scans available.",
                str(self),
                self.scans.count(),
                settings.MOON_TRACKER_MINIMUM_SCANS
            )
            return
        if self.get_annotation().final_scan is not None:
            logger.info(
                "Finalization already complete for %s.",
                str(self),
            )
            return

        logger.info("Finalization started for %s.", str(self))

        reference = self.scans.all()[0]
        ann = self.get_annotation()

        for scan in self.scans.all():
            if not reference.similar_to(scan):
                ann.final_scan = None
                ann.alert = True
                logger.warning("Dissimilar scan results found for %s.", str(self))
                break
        else:
            ann.final_scan = reference
            ann.alert = False
            logger.info("Finalization complete for %s.", str(self))

        ann.save()


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

    def get_ore_dict(self):
        return {o.ore_id: o.quantity for o in self.scanresultore_set.all()}

    def similar_to(self, other):
        d1 = self.get_ore_dict()
        d2 = other.get_ore_dict()

        if set(d1.keys()) != set(d2.keys()):
            return False

        for k in d1.keys():
            if not math.isclose(d1[k], d2[k], abs_tol=0.01):
                return False

        return True

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
