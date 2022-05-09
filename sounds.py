import math
from player import distance


def set_waterfall_volume(waterfall, hero, max_distance):
    waterfall_volume = abs(math.cos(math.radians(distance(waterfall, hero)*90/max_distance)))
    if distance(waterfall, hero) > max_distance:
        waterfall_volume = 0
    return waterfall_volume

