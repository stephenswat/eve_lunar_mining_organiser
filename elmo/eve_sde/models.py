from django.db import models

import roman


class Region(models.Model):
    id = models.IntegerField(primary_key=True)

    name = models.CharField(
        db_index=True,
        unique=True,
        max_length=64
    )

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()


class Constellation(models.Model):
    id = models.IntegerField(primary_key=True)

    region = models.ForeignKey(
        Region,
        related_name='constellations',
        db_index=True)

    name = models.CharField(
        db_index=True,
        unique=True,
        max_length=64
    )

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()


class SolarSystem(models.Model):
    id = models.IntegerField(primary_key=True)

    constellation = models.ForeignKey(
        Constellation,
        related_name='systems',
        db_index=True
    )

    name = models.CharField(
        db_index=True,
        unique=True,
        max_length=64
    )

    security = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()


class Planet(models.Model):
    id = models.IntegerField(primary_key=True)

    system = models.ForeignKey(
        SolarSystem,
        related_name='planets',
        db_index=True
    )

    number = models.IntegerField(db_index=True)

    def as_roman(self):
        return roman.toRoman(self.number)

    def __str__(self):
        return "%s %d" % (str(self.system), self.number)

    class Meta:
        default_permissions = ()
        ordering = ('number',)


class Moon(models.Model):
    id = models.IntegerField(primary_key=True)

    planet = models.ForeignKey(
        Planet,
        related_name='moons',
        db_index=True
    )

    number = models.IntegerField(db_index=True)

    def __str__(self):
        return "%s - Moon %d" % (str(self.planet), self.number)

    class Meta:
        default_permissions = ()
        ordering = ('number',)
