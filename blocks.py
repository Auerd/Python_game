import pygame
Surface = pygame.Surface
Sprite = pygame.sprite.Sprite
Color = pygame.Color
Rect = pygame.Rect
animation_delay = 0.5

# Лучше не трогать
platform_width = 32
platform_height = 32
platform_height_width = (platform_width, platform_height)
platform_color = '#FF6262'


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
        self.image = pygame.transform.scale(pygame.image.load("tiles/Tiles/tile_0068.png"),
                                            (platform_width, platform_height))


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


# class BlockWaterFall(Sprite):
#     def __init__(self, x, y, frame):
#         Platform.__init__(self, x, y)
#         self.rect = Rect(x-platform_width, y-platform_height, platform_width*3, platform_height*3)
#         self.image = ANIMATION_WATERFALL[frame]
#         self.image.set_colorkey('#FAFAFA')
