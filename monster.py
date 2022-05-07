#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
