import pygame
import pyganim
from map import platform_width, platform_height
Surface = pygame.Surface
Sprite = pygame.sprite.Sprite
Color = pygame.Color
Rect = pygame.Rect
animation_delay = 500
empty_in_png = 6

# Лучше не трогать
platform_height_width = (platform_width, platform_height)
platform_color = '#FF6262'

number_of_tile = [33, 53]
ANIMATION_WATER = [pygame.transform.scale(pygame.image.load(f"tiles/Tiles/tile_00{number_of_tile[i]}.png"),
                                          (platform_width, platform_height)) for i in range(0, 2)]


class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("tiles/Tiles/tile_0002.png"),
                                            (platform_width, platform_height))
        self.rect = Rect(x, y, platform_width, platform_height)


class PlatformLeft(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.transform.scale(pygame.image.load("tiles/Tiles/tile_0001.png"),
                                            (platform_width, platform_height))


class PlatformRight(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.transform.scale(pygame.image.load("tiles/Tiles/tile_0003.png"),
                                            (platform_width, platform_height))


class PlatformMiddle(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.transform.scale(pygame.image.load("tiles/Tiles/tile_0000.png"),
                                            (platform_width, platform_height))


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("tiles/Tiles/tile_0068.png")
        self.image = pygame.transform.scale(self.image, (platform_width, platform_height))
        self.rect = Rect(x, y, platform_width, platform_height/2)


class Steelblock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.transform.scale(pygame.image.load("tiles/Tiles/tile_0029.png"),
                                            (platform_width, platform_height))


class BlockWin(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("blocks/Win.png")
        self.image.set_colorkey('#000000')


class BlockWater(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltanim = []
        self.image = Surface((platform_width, platform_height))
        for anim in ANIMATION_WATER:
            boltanim.append((anim, animation_delay))
        self.boltAnimWater = pyganim.PygAnimation(boltanim)
        self.boltAnimWater.play()
        self.image.set_colorkey('#000000')

    def update(self):
        self.image.fill(Color('#000000'))
        self.boltAnimWater.blit(self.image, (0, 0))
