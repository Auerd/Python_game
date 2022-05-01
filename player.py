import pyganim
import pygame
import time
import blocks
from map import total_level_width, total_level_height
import monster

# Всё всё всё можно изменять в эксперементальных целях
Surface = pygame.Surface
sprite = pygame.sprite
Color = pygame.Color
Rect = pygame.Rect
timer = pygame.time.Clock()
Jump_power = 5
Gravity = 0.35
move_speed = 5
width = 22
height = 32
color = '#666666'
move_extra_speed = 7.5
animation_delay = 50
animation_extra_speed_delay = 25

# Это анимации
animation_right = [f'player/r{i}.png' for i in range(1, 6)]
animation_left = [f'player/l{i}.png' for i in range(1, 6)]
animation_jump_left = [('player/jl.png', 0.1)]
animation_jump_right = [('player/jr.png', 0.1)]
animation_jump = [('player/j.png', 0.1)]
animation_stay = [('player/0.png', 0.1)]


# Сам игрок
class Player(sprite.Sprite):
    def __init__(self, x, y, winner):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = Surface((width, height))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, width, height)
        self.yvel = 0
        self.onGround = False
        self.image.set_colorkey(Color(color))
        self.stuck = None
        self.winner = winner

        # Анимация движения вправо
        boltanim = []
        for anim in animation_right:
            boltanim.append((anim, animation_delay))
        self.boltAnimRight = pyganim.PygAnimation(boltanim)
        self.boltAnimRight.play()

        # Анимация движения влево
        boltanim = []
        for anim in animation_left:
            boltanim.append((anim, animation_delay))
        self.boltAnimLeft = pyganim.PygAnimation(boltanim)
        self.boltAnimLeft.play()

        # Это, когда игрок стоит
        self.boltAnimStay = pyganim.PygAnimation(animation_stay)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))
        # Прыгает влево
        self.boltAnimJumpLeft = pyganim.PygAnimation(animation_jump_left)
        self.boltAnimJumpLeft.play()
        # Прыгает вправо
        self.boltAnimJumpRight = pyganim.PygAnimation(animation_jump_right)
        self.boltAnimJumpRight.play()
        # Прыгает на месте
        self.boltAnimJump = pyganim.PygAnimation(animation_jump)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms):

        if not self.onGround or self.stuck:
            self.yvel += Gravity

        if up:
            if self.onGround or self.stuck:
                self.yvel = -Jump_power
            self.image.fill(Color(color))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left and (self.onGround or self.xvel == 0 or self.stuck) and self.xvel > -move_speed:
            self.xvel -= move_speed / 4
        if self.xvel < 0:
            self.image.fill(Color(color))
            if not self.stuck:
                if up:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimLeft.blit(self.image, (0, 0))
            else:
                if up:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimStay.blit(self.image, (0, 0))

        if right and (self.onGround or self.xvel == 0 or self.stuck) and self.xvel < move_speed:
            self.xvel += move_speed / 4
        if self.xvel > 0:
            self.image.fill(Color(color))
            if not self.stuck:
                if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimRight.blit(self.image, (0, 0))
            else:
                if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimStay.blit(self.image, (0, 0))

        if not (left or right):
            if self.onGround:
                if self.xvel < 0:
                    self.xvel += move_speed / 4
                if self.xvel > 0:
                    self.xvel -= move_speed / 4
        if self.xvel == 0:
            if not up:
                self.image.fill(Color(color))
                self.boltAnimStay.blit(self.image, (0, 0))

        if self.rect.y >= total_level_height or self.rect.x >= total_level_width or self.rect.x <= 0:
            self.die()

        self.onGround = False
        self.stuck = False

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if xvel > 0:
                    self.stuck = True
                    self.rect.right = platform.rect.left
                if xvel < 0:
                    self.stuck = True
                    self.rect.left = platform.rect.right

                if yvel > 0:
                    self.rect.bottom = platform.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = platform.rect.bottom
                    self.yvel = 0
                    self.stuck = True
                if isinstance(platform, (blocks.BlockDie, monster.Monster)):
                    self.die()
                elif isinstance(platform, blocks.BlockWin):
                    self.win()

    def die(self):
        time.sleep(0.5)
        self.teleporting(self.startX, self.startY)
        self.xvel = 0
        self.yvel = 0

    def win(self):
        time.sleep(0.5)
        self.teleporting(self.startX, self.startY)
        self.winner = True

    def teleporting(self, gox, goy):
        self.rect.x = gox
        self.rect.y = goy
