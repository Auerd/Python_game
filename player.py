import random

import pyganim
import pygame
import time
import blocks
import monster
import math

# Всё всё всё можно изменять в эксперементальных целях
Coefficient = 60
Bigger = 1.5
Surface = pygame.Surface
sprite = pygame.sprite
Color = pygame.Color
Rect = pygame.Rect
timer = pygame.time.Clock()
Jump_power = 6
Gravity = 0.35
move_speed = 5
width = int(22 * Bigger)
height = int(32 * Bigger)
color = '#666666'
move_speed_shift = move_speed/4
animation_delay = 50
animation_extra_speed_delay = 25

transform = pygame.transform
image = pygame.image

# Это анимации
animation_right = [pygame.transform.scale(
    pygame.image.load(f'player2/p1_walk/PNG/p1_walk0{i}.png'),
    (width, height))
                   for i in range(1, 6)]
animation_left = [pygame.transform.flip(
    pygame.transform.scale(
        pygame.image.load(f'player2/p1_walk/PNG/p1_walk0{i}.png'),
        (width, height)),
    True, False)
                  for i in range(1, 6)]
animation_jump_right = [(transform.scale(image.load('player2/p1_jump.png'), (width, height)), 0.1)]
animation_jump_left = [(transform.flip(animation_jump_right[0][0], True, False), 0.1)]
animation_jump = [(transform.scale(image.load('player2/p1_front.png'), (width, height)), 0.1)]
animation_stay = animation_jump
animation_stay_right = [(transform.scale(image.load('player2/p1_stand.png'), (width, height)), 0.1)]
animation_stay_left = [(transform.flip(animation_stay_right[0][0], True, False), 0.1)]
animation_hurt_right = [(transform.scale(image.load('player2/p1_hurt.png'), (width, height)), 0.1)]
animation_hurt_left = [(transform.flip(animation_hurt_right[0][0], True, False), 0.1)]


def distance(obj_1, obj_2):
    obj_1_x = obj_1.rect.x + obj_1.rect.width/2
    obj_1_y = obj_1.rect.y + obj_1.rect.height/2
    obj_2_x = obj_2.rect.x + obj_2.rect.width/2
    obj_2_y = obj_2.rect.y + obj_2.rect.height/2
    distance_now = math.sqrt((obj_1_x - obj_2_x) * (obj_1_x - obj_2_x) + (obj_1_y - obj_2_y) * (obj_1_y - obj_2_y))
    return distance_now


# Сам игрок
class Player(sprite.Sprite):
    def __init__(self, x, y, winner, level_width, level_height):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = Surface((width, height))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, width, height)
        self.yvel = 0
        self.onGround = None
        self.image.set_colorkey(Color(color))
        self.stuck = None
        self.winner = winner
        self.did = False
        self.right_stop = 0
        self.left_stop = 0
        self.level_width = level_width
        self.level_height = level_height
        self.hurt = False
        self.timer_hurt = False
        self.time_hurt = time.time()
        self.lifes = 6

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
        # Стоит вправо
        self.boltAnimStayRight = pyganim.PygAnimation(animation_stay_right)
        self.boltAnimStayRight.play()
        # Стоит влево
        self.boltAnimStayLeft = pyganim.PygAnimation(animation_stay_left)
        self.boltAnimStayLeft.play()
        # Прыгает влево
        self.boltAnimJumpLeft = pyganim.PygAnimation(animation_jump_left)
        self.boltAnimJumpLeft.play()
        # Прыгает вправо
        self.boltAnimJumpRight = pyganim.PygAnimation(animation_jump_right)
        self.boltAnimJumpRight.play()
        # Прыгает на месте
        self.boltAnimJump = pyganim.PygAnimation(animation_jump)
        self.boltAnimJump.play()

        self.boltAnimHurtRight = pyganim.PygAnimation(animation_hurt_right)
        self.boltAnimHurtRight.play()

        self.boltAnimHurtLeft = pyganim.PygAnimation(animation_hurt_left)
        self.boltAnimHurtLeft.play()

    def update(self, left, right, up, platforms, FPS, entities):
        time_real = time.time()
        if not self.onGround or self.stuck:
            self.yvel += Gravity

        if up:
            if self.onGround or self.stuck:
                self.yvel = -Jump_power
                self.image.fill(Color(color))
                self.boltAnimJump.blit(self.image, (0, 0))
                self.right_stop = self.left_stop = False

        if self.timer_hurt:
            self.time_hurt = time.time()
            self.timer_hurt = False

        self.hurt = time_real - self.time_hurt < 0.5

        if self.xvel != 0:
            self.right_stop = self.left_stop = False

        if left and (self.onGround or self.xvel == 0 or self.stuck):
            if self.xvel > -move_speed:
                self.xvel -= move_speed / 4

        if self.xvel < 0:
            self.image.fill(Color(color))
            if self.hurt:
                self.boltAnimHurtRight.blit(self.image, (0, 0))
            elif not self.stuck:
                if up:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimLeft.blit(self.image, (0, 0))
            else:
                if up:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimStay.blit(self.image, (0, 0))

        if right and (self.onGround or self.xvel == 0 or self.stuck):
            if self.xvel < move_speed:
                self.xvel += move_speed / 4

        if self.xvel > 0:
            self.image.fill(Color(color))
            if self.hurt:
                self.boltAnimHurtLeft.blit(self.image, (0, 0))
            elif not self.stuck:
                if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimRight.blit(self.image, (0, 0))
            else:
                if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimStay.blit(self.image, (0, 0))

        if not (left or right) and self.onGround:
            if self.xvel < 0:
                self.xvel += move_speed / 4
                if -move_speed / 4 < self.xvel < move_speed / 4:
                    self.xvel = 0
                    self.left_stop = True

            if self.xvel > 0:
                self.xvel -= move_speed / 4
                if -move_speed / 4 < self.xvel < move_speed / 4:
                    self.xvel = 0
                    self.right_stop = True

        if -self.rect.height * 1.1 >= self.rect.y or \
                self.rect.y >= self.level_height or \
                self.rect.x <= -self.rect.width or \
                self.rect.x >= self.level_width:
            self.die()

        if self.right_stop:
            self.image.fill(Color(color))
            self.boltAnimStayRight.blit(self.image, (0, 0))
        elif self.left_stop:
            self.image.fill(Color(color))
            self.boltAnimStayLeft.blit(self.image, (0, 0))
        elif not(self.left_stop or self.right_stop) and self.xvel == 0:
            self.image.fill(Color(color))
            self.boltAnimStay.blit(self.image, (0, 0))

        self.onGround = False
        self.stuck = False

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, entities)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, entities)

    def collide(self, xvel, yvel, platforms, entities):
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
                if isinstance(platform, blocks.BlockDie) and not self.stuck:
                    self.hurt_from_block()
                    self.timer_hurt = True
                    self.lifes -= 1
                elif isinstance(platform, monster.MovingObject):
                    if platform.move_speed_y < 0:
                        self.yvel = -1
                    if platform.move_speed_x > 0:
                        self.xvel += 0.3
                    elif platform.move_speed_x < 0:
                        self.xvel -= 0.3
        # for entity in entities:
        #     if sprite.collide_rect(self, entity):
        #         if xvel > 0 and isinstance(entity, blocks.Ladder):
        #             self.stuck = True
        #         if xvel < 0 and isinstance(entity, blocks.Ladder):
        #             self.stuck = True

    def die(self):
        time.sleep(0.5)
        self.teleporting(self.startX, self.startY)
        self.lifes -= 2
        if self.lifes >= 1:
            self.xvel = 0
            self.yvel = 0

    def hurt_from_block(self):
        self.yvel = random.randint(-Jump_power*12, -Jump_power*5)/10
        self.xvel = random.randint(-move_speed*2, move_speed*2)

    def win(self):
        time.sleep(0.5)
        self.teleporting(self.startX, self.startY)
        self.winner = True

    def teleporting(self, gox, goy):
        self.rect.x = gox
        self.rect.y = goy
