#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyganim
import pygame
from map import platform_width, platform_height

ANIMATION_DELAY = 300
COLOR = "#000000"
COIN_ANIMATION = [pygame.transform.scale(
    pygame.image.load(f"tiles/Tiles/tile_015{i}.png"),
    (platform_width, platform_height))
    for i in range(1, 3)]


# class Monster(pygame.sprite.Sprite):
#     def __init__(self, x, y, left, up, max_length_up):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load("blocks/Untitled-1.png")
#         self.rect = pygame.Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
#         self.startX = x  # начальные координаты
#         self.startY = y
#         self.maxLengthUp = max_length_up  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
#         self.xvel = left  # скорость передвижения по горизонтали, 0 - стоит на месте
#         self.yvel = up  # скорость движения по вертикали, 0 - не двигается
#
#     def update(self, platforms):  # по принципу героя
#
#         self.rect.y += self.yvel
#         self.rect.x += self.xvel
#
#         self.collide(platforms)
#
#         if abs(self.startY - self.rect.y) > self.maxLengthUp:
#             self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль
#
#     def collide(self, platforms):
#         for p in platforms:
#             if pygame.sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
#                 self.xvel = - self.xvel  # то поворачиваем в обратную сторону
#                 self.yvel = - self.yvel
#

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, up):
        pygame.sprite.Sprite.__init__(self)
        boltanim = []
        self.image = pygame.Surface((platform_width, platform_height))
        self.image.fill(pygame.Color(COLOR))
        self.image.set_colorkey(COLOR)
        for anim in COIN_ANIMATION:
            boltanim.append((anim, ANIMATION_DELAY))
        self.boltAnimRound = pyganim.PygAnimation(boltanim)
        self.boltAnimRound.play()
        self.rect = pygame.Rect(x, y, platform_width, platform_height)
        self.startX = x
        self.startY = y
        self.maxLengthUp = platform_height/5
        self.yvel = up

    def update(self):  # по принципу героя
        self.rect.y += self.yvel
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = -self.yvel
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimRound.blit(self.image, (0, 0))
