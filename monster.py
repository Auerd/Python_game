import pyganim
import pygame
from map import platform_width, platform_height
import random

COLOR = "#000000"
COIN_ANIMATION = [pygame.transform.scale(
    pygame.image.load(f"tiles/Tiles/tile_015{i}.png"),
    (platform_width, platform_height))
    for i in range(1, 3)]


class Coin(pygame.sprite.Sprite):
    def __init__(self, rect, up):
        ANIMATION_DELAY = random.randint(275, 325)
        pygame.sprite.Sprite.__init__(self)
        boltanim = []
        self.image = pygame.Surface((platform_width, platform_height))
        self.image.fill(pygame.Color(COLOR))
        self.image.set_colorkey(COLOR)
        for anim in COIN_ANIMATION:
            boltanim.append((anim, ANIMATION_DELAY))
        self.boltAnimRound = pyganim.PygAnimation(boltanim)
        self.boltAnimRound.play()
        self.rect = rect
        self.startX = self.rect.x
        self.startY = self.rect.y
        self.maxLengthUp = platform_height/5
        self.yvel = up

    def update(self):
        self.rect.y += self.yvel
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = -self.yvel
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimRound.blit(self.image, (0, 0))


class MovingObject(pygame.sprite.Sprite):
    def __init__(self, rect, image, to_coord, steps):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rect
        self.stx = self.rect.x
        self.sty = self.rect.y
        self.tox = to_coord[0]
        self.toy = to_coord[1]
        self.path = (-(self.rect.y - self.toy), -(self.rect.x - self.tox))
        self.move_speed_y = self.path[0]
        self.move_speed_x = self.path[1]
        if self.move_speed_x > 0:
            self.move_speed_x = 1
        elif self.move_speed_x < 0:
            self.move_speed_x = -1
        if self.move_speed_y > 0:
            self.move_speed_y = 1
        elif self.move_speed_y < 0:
            self.move_speed_y = -1
        self.up = self.move_speed_y < 0
        self.left = self.move_speed_x < 0
        self.steps = steps

    def update(self):
        self.rect.y += self.move_speed_y
        self.rect.x += self.move_speed_x
        if self.up and (self.toy >= self.rect.y or self.sty <= self.rect.y):
            self.move_speed_y = -self.move_speed_y
        if not self.up and (self.toy <= self.rect.y or self.sty >= self.rect.y):
            self.move_speed_y = -self.move_speed_y
        if self.left and (self.tox >= self.rect.x or self.stx <= self.rect.x):
            self.move_speed_x = -self.move_speed_x
        if not self.left and (self.tox <= self.rect.x or self.stx >= self.rect.x):
            self.move_speed_x = -self.move_speed_x
