import pygame
from levels import levels
from map import maps, platform_width, platform_height
from player import Player, distance_is
from blocks import Platform, BlockDie, BlockWin, Steelblock, PlatformLeft, PlatformRight, PlatformMiddle, BlockWater
import Camera as c
import time
from monster import Coin


 # Высота
win_width = 1000
win_height = 640
display = (win_width, win_height)  # Дисплей

background_color = '#004400'


def main():
    # Частота кадров которую мы хотим
    # need_fps = int(input("Введите частоту кадров: "))
    need_fps = 60
    # Ширина высота первого уровня
    total_level_width = len(levels[0][0]) * platform_width
    total_level_height = len(levels[0]) * platform_height
    # Определяем игрока
    hero = Player(55, 55, 0)
    # Инициализация пайгейм
    down = left = right = up = False
    run = True
    pygame.init()
    # Экран
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption('хз пока что за игра')
    # Задний фон
    screen.set_alpha(None)
    # Камера
    camera = c.Camera(total_level_width, total_level_height, win_width, win_height)
    # Задний фон
    prop = 1.4
    bg = pygame.image.load('bg/hCUwLQ.png')
    bg = pygame.transform.scale(bg, (int(bg.get_width()*prop), int(bg.get_height()*prop)))
    # Счётчики
    count_win = 0
    frames = 0
    new_time = time.time()
    FPS = 180
    tick = 60
    entities_on_maps = []
    platforms_on_maps = []
    animated_entities_on_maps = []
    coins = 0
    # Переключатель между картами + иницализация недвижимых объектов на карте
    for k in range(len(maps)):
        animated_entities = pygame.sprite.Group()
        entities = pygame.sprite.Group()
        platforms = []
        entities.add(hero)
        for i in maps[k]:
            if i[2] == 'platform':
                pf = Platform(i[0], i[1])
                entities.add(pf)
                platforms.append(pf)
            elif i[2] == "W":
                bw = BlockWater(i[0], i[1])
                entities.add(bw)
                animated_entities.add(bw)
            elif i[2] == 'blockwin':
                bw = BlockWin(i[0], i[1])
                entities.add(bw)
                platforms.append(bw)
            elif i[2] == 'blockdie':
                bd = BlockDie(i[0], i[1])
                platforms.append(bd)
                entities.add(bd)
            elif i[2] == 'steelblock':
                sb = Steelblock(i[0], i[1])
                entities.add(sb)
                platforms.append(sb)
            elif i[2] == 'platform_l':
                pl = PlatformLeft(i[0], i[1])
                entities.add(pl)
                platforms.append(pl)
            elif i[2] == 'platform_r':
                pr = PlatformRight(i[0], i[1])
                entities.add(pr)
                platforms.append(pr)
            elif i[2] == 'platform_m':
                pm = PlatformMiddle(i[0], i[1])
                entities.add(pm)
                platforms.append(pm)
            elif i[2] == "C":
                cn = Coin(i[0], i[1], 1)
                entities.add(cn)
                animated_entities.add(cn)
        entities_on_maps.append(entities)
        platforms_on_maps.append(platforms)
        animated_entities_on_maps.append(animated_entities)
    while run:
        timer = pygame.time.Clock()
        timer.tick(64)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            if i.type == pygame.KEYDOWN and i.key == pygame.K_a:
                left = True
            elif i.type == pygame.KEYUP and i.key == pygame.K_a:
                left = False
            if i.type == pygame.KEYDOWN and i.key == pygame.K_d:
                right = True
            elif i.type == pygame.KEYUP and i.key == pygame.K_d:
                right = False
            if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
                up = True
            elif i.type == pygame.KEYUP and i.key == pygame.K_SPACE:
                up = False
            if i.type == pygame.KEYDOWN and i.key == pygame.K_s:
                down = True
            elif i.type == pygame.KEYUP and i.key == pygame.K_s:
                down = False
        # Создаём группу сущностей и список объектов и создаём в ней героя

        if hero.winner:
            count_win += 1
            hero.winner = 0
            total_level_width = len(levels[count_win][0]) * platform_width
            total_level_height = len(levels[count_win]) * platform_height
            camera = c.Camera(total_level_width, total_level_height,
                              min(win_width, total_level_width),
                              min(win_height, total_level_height))

        frames += 1
        real_time = time.time()
        # частота обновления кадров
        if real_time - new_time > 1:
            new_time = time.time()
            FPS = frames
            print(FPS)
            if FPS < need_fps:
                tick += 1
            elif FPS > need_fps:
                tick -= 1
            frames = 0

        # обновление анимированных объектов
        if frames % 3 == 0:
            animated_entities_on_maps[count_win].update()
        # Параллакс
        screen.blit(bg, ((camera.state.x - bg.get_width()/2)/2, 0))
        # прорисовка всех объектов
        for entity in entities_on_maps[count_win]:
            screen.blit(entity.image, camera.apply(entity))
            if type(entity) == Coin and distance_is(25, entity, hero):
                coins += 1
                entity.kill()

        # прорисовка главного героя
        camera.update(hero)
        # обновление показаний главного героя
        hero.update(left, right, up, down, platforms_on_maps[count_win], FPS)
        # обновление экрана
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
