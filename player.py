import pyganim
import pygame
import time
import blocks
from map import total_level_width, total_level_height
import monster

# Всё всё всё можно изменять в эксперементальных целях
Coefficient = 60
Bigger = 1.2
Surface = pygame.Surface
sprite = pygame.sprite
Color = pygame.Color
Rect = pygame.Rect
timer = pygame.time.Clock()
Jump_power = 5.5
Gravity = 0.35
move_speed = 5
width = int(22 * Bigger)
height = int(32 * Bigger)
shift_height = int((32 * Bigger) / 1.3)
color = '#666666'
move_speed_shift = move_speed/4
animation_delay = 50
animation_extra_speed_delay = 25

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
animation_jump_right = [(pygame.transform.scale(pygame.image.load('player2/p1_jump.png'), (width, height)), 0.1)]
animation_jump_left = [(pygame.transform.flip(animation_jump_right[0][0], True, False), 0.1)]
animation_jump = [(pygame.transform.scale(pygame.image.load('player2/p1_front.png'), (width, height)), 0.1)]
animation_stay = animation_jump
animation_stay_right = [(pygame.transform.scale(pygame.image.load('player2/p1_stand.png'), (width, height)), 0.1)]
animation_stay_left = [(pygame.transform.flip(animation_stay_right[0][0], True, False), 0.1)]
animation_shift_right = [(pygame.transform.scale(pygame.image.load('player2/p1_duck.png'), (width, shift_height)), 0.1)]
animation_shift_left = [(pygame.transform.flip(animation_shift_right[0][0], True, False), 0.1)]


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
        self.onGround = None
        self.image.set_colorkey(Color(color))
        self.stuck = None
        self.winner = winner
        self.did = False
        self.right_stop = 0
        self.left_stop = 0

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
        # Приседает влево
        self.boltAnimShiftLeft = pyganim.PygAnimation(animation_shift_left)
        self.boltAnimShiftLeft.play()
        # Приседает вправо
        self.boltAnimShiftRight = pyganim.PygAnimation(animation_shift_right)
        self.boltAnimShiftRight.play()

    def update(self, left, right, up, down, platforms, FPS):
        if not self.onGround or self.stuck:
            self.yvel += Gravity

        if up:
            if self.onGround or self.stuck:
                self.yvel = -Jump_power
                self.image.fill(Color(color))
                self.boltAnimJump.blit(self.image, (0, 0))
                self.right_stop = self.left_stop = False

        if self.xvel != 0:
            self.right_stop = self.left_stop = False

        if left and (self.onGround or self.xvel == 0 or self.stuck):
            if not down and self.xvel > -move_speed:
                self.xvel -= move_speed / 4
            elif self.xvel > -move_speed_shift:
                self.xvel -= move_speed_shift / 4
            elif self.xvel < move_speed_shift:
                self.xvel += move_speed_shift / 4

        if self.xvel < 0:
            self.image.fill(Color(color))
            if not self.stuck:
                if up:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                elif down:
                    self.boltAnimShiftLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimLeft.blit(self.image, (0, 0))
            else:
                if up:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimStay.blit(self.image, (0, 0))

        if right and (self.onGround or self.xvel == 0 or self.stuck):
            if not down and self.xvel < move_speed:
                self.xvel += move_speed / 4
            elif self.xvel < move_speed_shift:
                self.xvel += move_speed_shift / 4
            elif self.xvel > move_speed_shift:
                self.xvel -= move_speed_shift / 4

        if self.xvel > 0:
            self.image.fill(Color(color))
            if not self.stuck:
                if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                elif down:
                    self.boltAnimShiftRight.blit(self.image, (0, 0))
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
                self.rect.y >= total_level_height or \
                self.rect.x <= self.rect.width or \
                self.rect.x >= total_level_width:
            self.die()

        if down and self.onGround:
            if not self.did:
                self.rect.height = shift_height
                # self.rect.y += height - shift_height
            self.did = True
        elif not down:
            if self.did:
                self.rect.height = height
                # self.rect.y += height - shift_height
            self.did = False

        if not(up or down) and self.right_stop:
            self.image.fill(Color(color))
            self.boltAnimStayRight.blit(self.image, (0, 0))
        elif down and self.right_stop:
            self.image.fill(Color(color))
            self.boltAnimShiftRight.blit(self.image, (0, 0))
        if not(up or down) and self.left_stop:
            self.image.fill(Color(color))
            self.boltAnimStayLeft.blit(self.image, (0, 0))
        elif down and self.left_stop:
            self.image.fill(Color(color))
            self.boltAnimShiftLeft.blit(self.image, (0, 0))

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
