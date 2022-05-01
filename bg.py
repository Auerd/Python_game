import pygame
Sprite = pygame.sprite.Sprite


scale = 2.2
bg_width = int(500*scale)
bg_height = int(288*scale)
bg_height_width = (bg_width, bg_height)


class BackGround(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.images = [pygame.transform.scale(
        #     pygame.image.load(f'bg/{i}.gif'),
        #     bg_height_width)
        #     for i in range(0, 6)
        #               ]

        self.image = pygame.image.load('bg/maxresdefault.jpg')
        # self.main_x = x + self.image.get_width()
        # self.main_y = y + self.image.get_height()
        # self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
