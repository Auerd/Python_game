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
    def __init__(self, rect, image):
        Sprite.__init__(self)
        self.image = image
        self.rect = rect


class BlockDie(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, platform_width, platform_height/2)
        self.image = pygame.image.load('tiles/Tiles/tile_0068.png')
        self.image = pygame.transform.scale(self.image, (platform_width, platform_height))


class Ladder(Platform):
    def __init__(self, rect, image):
        Platform.__init__(self, rect, image)


class BlockWin(Platform):
    def __init__(self, rect, image):
        Platform.__init__(self, rect, image)


class AlphaEntity(Platform):
    def __init__(self, rect, image):
        Platform.__init__(self, rect, image)

    def update(self):
        self.image.set_alpha(200)


class Water(Sprite):
    def __init__(self, rect, animation):
        Sprite.__init__(self)
        boltanim = []
        self.image = Surface((platform_width, platform_height))
        for anim in animation:
            boltanim.append((anim, animation_delay))
        self.boltAnimWater = pyganim.PygAnimation(boltanim)
        self.boltAnimWater.play()
        self.rect = rect
        self.image.set_colorkey('#000000')

    def update(self):
        self.image.fill(Color('#000000'))
        self.image.set_alpha(200)
        self.boltAnimWater.blit(self.image, (0, 0))
