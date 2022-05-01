#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#2110FF"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, left, up, max_length_up):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("blocks/Untitled-1.png")
        self.rect = pygame.Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthUp = max_length_up  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается

    def update(self, platforms):  # по принципу героя

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel
