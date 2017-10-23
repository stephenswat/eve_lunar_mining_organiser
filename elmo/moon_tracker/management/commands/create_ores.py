from django.core.management.base import BaseCommand

from moon_tracker.models import Ore, Mineral, OreMineral


ORE_CHOICES = (
    (46675, 8.00, 'Dark Ochre', 'standard'),
    (46676, 16.0, 'Bistot', 'standard'),
    (46677, 16.0, 'Crokite', 'standard'),
    (46678, 16.0, 'Arkonor', 'standard'),
    (46679, 5.00, 'Gneiss', 'standard'),
    (46680, 3.00, 'Hedbergite', 'standard'),
    (46681, 3.00, 'Hemorphite', 'standard'),
    (46682, 2.00, 'Jaspet', 'standard'),
    (46683, 1.20, 'Kernite', 'standard'),
    (46684, 0.60, 'Omber', 'standard'),
    (46685, 0.35, 'Plagioclase', 'standard'),
    (46686, 0.30, 'Pyroxeres', 'standard'),
    (46687, 0.15, 'Scordite', 'standard'),
    (46688, 16.0, 'Spodumain', 'standard'),
    (46689, 0.10, 'Veldspar', 'standard'),

    (45490, 10.0, 'Zeolites', 'ubiquitous'),
    (45491, 10.0, 'Sylvites', 'ubiquitous'),
    (45492, 10.0, 'Bitumens', 'ubiquitous'),
    (45493, 10.0, 'Coesite', 'ubiquitous'),

    (45494, 10.0, 'Cobaltite', 'common'),
    (45495, 10.0, 'Euxenite', 'common'),
    (45496, 10.0, 'Titanite', 'common'),
    (45497, 10.0, 'Scheelite', 'common'),

    (45498, 10.0, 'Otavite', 'uncommon'),
    (45499, 10.0, 'Sperrylite', 'uncommon'),
    (45500, 10.0, 'Vanadinite', 'uncommon'),
    (45501, 10.0, 'Chromite', 'uncommon'),

    (45502, 10.0, 'Carnotite', 'rare'),
    (45503, 10.0, 'Zircon', 'rare'),
    (45504, 10.0, 'Pollucite', 'rare'),
    (45506, 10.0, 'Cinnabar', 'rare'),

    (45510, 10.0, 'Xenotime', 'exceptional'),
    (45511, 10.0, 'Monazite', 'exceptional'),
    (45512, 10.0, 'Loparite', 'exceptional'),
    (45513, 10.0, 'Ytterbite', 'exceptional'),
)


MINERAL_CHOICES = (
    (34, 'Tritanium', 'mineral'),
    (35, 'Pyerite', 'mineral'),
    (36, 'Mexallon', 'mineral'),
    (37, 'Isogen', 'mineral'),
    (38, 'Nocxium', 'mineral'),
    (39, 'Zydrine', 'mineral'),
    (40, 'Megacyte', 'mineral'),
    (11399, 'Morphite', 'mineral'),

    (16634, 'Atmospheric Gases', 'r4'),
    (16635, 'Evaporite Deposits', 'r4'),
    (16633, 'Hydrocarbons', 'r4'),
    (16636, 'Silicates', 'r4'),

    (16640, 'Cobalt', 'r8'),
    (16639, 'Scandium', 'r8'),
    (16638, 'Titanium', 'r8'),
    (16637, 'Tungsten', 'r8'),

    (16643, 'Cadmium', 'r16'),
    (16641, 'Chromium', 'r16'),
    (16644, 'Platinum', 'r16'),
    (16642, 'Vanadium', 'r16'),

    (16647, 'Caesium', 'r32'),
    (16648, 'Hafnium', 'r32'),
    (16646, 'Mercury', 'r32'),
    (16649, 'Technetium', 'r32'),

    (16650, 'Dysprosium', 'r64'),
    (16651, 'Neodymium', 'r64'),
    (16652, 'Promethium', 'r64'),
    (16653, 'Thulium', 'r64'),
)

YIELDS = {
    46675: {34: 11500, 37: 1840, 38: 138},
    46676: {34: 13800, 39: 518, 40: 115},
    46677: {34: 24150, 38: 874, 39: 155},
    46678: {34: 25300, 36: 2875, 40: 368},
    46679: {35: 2530, 36: 2760, 37: 345},
    46680: {35: 1150, 37: 230, 38: 115, 39: 22},
    46681: {34: 2530, 37: 115, 38: 138, 39: 17},
    46682: {36: 403, 38: 86, 39: 9},
    46683: {34: 154, 36: 307, 37: 154},
    46684: {34: 920, 35: 115, 37: 98},
    46685: {34: 123, 35: 245, 36: 123},
    46686: {34: 404, 35: 29, 36: 58, 38: 6},
    46687: {34: 398, 35: 199},
    46688: {34: 64400, 35: 13858, 36: 2415, 37: 518},
    46689: {34: 477},

    45490: {34: 4000, 35: 8000, 36: 400, 16634: 65},
    45491: {34: 8000, 35: 4000, 36: 400, 16635: 65},
    45492: {34: 6000, 35: 6000, 36: 400, 16633: 65},
    45493: {34: 10000, 35: 2000, 36: 400, 16636: 65},

    45494: {34: 7500, 35: 10000, 36: 500, 16640: 40},
    45495: {34: 10000, 35: 7500, 36: 500, 16639: 40},
    45496: {34: 15000, 35: 2500, 36: 500, 16638: 40},
    45497: {34: 12500, 35: 5000, 36: 500, 16637: 40},

    45498: {34: 5000, 36: 1500, 37: 500, 38: 50, 16634: 10, 16643: 40},
    45499: {34: 5000, 36: 1000, 37: 1000, 38: 50, 16635: 10, 16644: 40},
    45500: {35: 5000, 36: 750, 37: 1250, 39: 50, 16636: 10, 16642: 40},
    45501: {35: 5000, 36: 1250, 37: 750, 38: 50, 16633: 10, 16641: 40},

    45502: {36: 1000, 37: 1250, 39: 50, 16634: 15, 16640: 10, 16649: 50},
    45503: {36: 1750, 37: 500, 40: 50, 16636: 15, 16638: 10, 16648: 50},
    45504: {36: 1250, 37: 1000, 39: 50, 16633: 15, 16639: 10, 16647: 50},
    45506: {36: 1500, 37: 750, 40: 50, 16635: 15, 16637: 10, 16646: 50},

    45510: {38: 200, 39: 100, 40: 50, 16634: 20, 16640: 20, 16642: 10, 16650: 22},
    45511: {38: 50, 39: 150, 40: 150, 16635: 20, 16637: 20, 16641: 10, 16651: 22},
    45512: {38: 100, 39: 200, 40: 50, 16633: 20, 16639: 20, 16644: 10, 16652: 22},
    45513: {38: 50, 39: 100, 40: 200, 16636: 20, 16638: 20, 16643: 10, 16653: 22},
}

class Command(BaseCommand):
    help = 'Creates ore and mineral records.'

    def handle(self, *args, **options):
        Ore.objects.all().delete()
        Mineral.objects.all().delete()
        OreMineral.objects.all().delete()
        self.create_ores()
        self.create_minerals()
        self.create_yields()

    def create_ores(self):
        for i, v, n, r in ORE_CHOICES:
            Ore.objects.get_or_create(
                id=i,
                name=n,
                rarity=r,
                volume=v
            )

    def create_minerals(self):
        for i, n, r in MINERAL_CHOICES:
            Mineral.objects.get_or_create(
                id=i,
                name=n,
                rarity=r
            )

    def create_yields(self):
        for o, c in YIELDS.items():
            ore = Ore.objects.get(id=o)

            for m, q in c.items():
                OreMineral.objects.get_or_create(
                    ore=ore,
                    mineral_id=m,
                    quantity=int(q / ore.volume)
                )
