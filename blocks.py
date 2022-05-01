import pygame
import pyganim
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
ANIMATION_WATERFALL = [pygame.transform.scale(pygame.image.load(f'bg/frame-{i} — копия.png'),
                                              (platform_width*3, platform_height*2))
                       for i in range(1, 7)]


class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load("blocks/2png-transbrick-mario.png")
        self.rect = Rect(x, y, platform_width, platform_height)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("blocks/Untitled-1.png")
        self.image.set_colorkey('#000000')


class Steelblock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("blocks/Steelblock.png")
        self.image.set_colorkey('#FFFFFF')


class BlockWin(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("blocks/Win.png")
        self.image.set_colorkey('#000000')


class BlockWaterFall(Sprite):
    def __init__(self, x, y, frame):
        Platform.__init__(self, x, y)
        # boltanim = []
        # for anim in ANIMATION_WATERFALL:
        #     boltanim.append((anim, animation_delay))
        # self.boltAnim_fall = pyganim.PygAnimation(boltanim)
        # self.boltAnim_fall.play()
        self.rect = Rect(x-platform_width, y-platform_height, platform_width*3, platform_height*3)
        # self.image = Surface((platform_width*3, platform_height*2))
        self.image = ANIMATION_WATERFALL[frame]
        self.image.set_colorkey('#FAFAFA')
