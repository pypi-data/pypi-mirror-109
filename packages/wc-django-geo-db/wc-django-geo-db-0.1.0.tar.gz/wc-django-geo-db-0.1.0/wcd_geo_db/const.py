from django.db import models
from django.utils.translation import pgettext_lazy


class DivisionLevel(models.IntegerChoices):
    COUNTRY = 1200, pgettext_lazy('wcd_geo_db', 'Country')

    ADMINISTRATIVE_LEVEL_1 = 1410, pgettext_lazy('wcd_geo_db', 'Administrative division: Level 1')
    ADMINISTRATIVE_LEVEL_2 = 1420, pgettext_lazy('wcd_geo_db', 'Administrative division: Level 2')
    ADMINISTRATIVE_LEVEL_3 = 1430, pgettext_lazy('wcd_geo_db', 'Administrative division: Level 3')
    ADMINISTRATIVE_LEVEL_4 = 1440, pgettext_lazy('wcd_geo_db', 'Administrative division: Level 4')
    ADMINISTRATIVE_LEVEL_5 = 1450, pgettext_lazy('wcd_geo_db', 'Administrative division: Level 5')

    LOCALITY = 1600, pgettext_lazy('wcd_geo_db', 'Locality')

    SUBLOCALITY_LEVEL_1 = 1810, pgettext_lazy('wcd_geo_db', 'Locality division: Level 1')
    SUBLOCALITY_LEVEL_2 = 1820, pgettext_lazy('wcd_geo_db', 'Locality division: Level 2')
    SUBLOCALITY_LEVEL_3 = 1830, pgettext_lazy('wcd_geo_db', 'Locality division: Level 3')
    SUBLOCALITY_LEVEL_4 = 1840, pgettext_lazy('wcd_geo_db', 'Locality division: Level 4')
    SUBLOCALITY_LEVEL_5 = 1850, pgettext_lazy('wcd_geo_db', 'Locality division: Level 5')
