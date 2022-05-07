import pygame
from levels import levels
from map import maps, platform_width, platform_height
from player import Player, distance_is
from blocks import Platform, Water
import Camera as c
import time
from monster import Coin
from counter import coin_counter, fps_counter


 # Высота
win_width = 1000
win_height = 640
display = (win_width, win_height)  # Дисплей

background_color = '#004400'


def main():
    # Частота кадров которую мы хотим
    # need_fps = int(input("Введите частоту кадров: "))
    Size_map = levels[0].map_size
    need_fps = 60
    # Определяем игрока
    total_level_height, total_level_width = Size_map.height*platform_height, Size_map.width*platform_width
    # Инициализация пайгейм
    left = right = up = False
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
    prop = 1.8
    bg = pygame.image.load('bg/hCUwLQ.png')
    bg = pygame.transform.scale(bg, (int(bg.get_width()*prop), int(bg.get_height()*prop)))
    # Счётчики
    count_win = 0
    frames = 0
    new_time = time.time()
    FPS = 180
    tick = 60
    player_coordinates = []
    entities_on_maps = []
    platforms_on_maps = []
    animated_entities_on_maps = []
    coins = 0
    # Переключатель между картами + иницализация недвижимых объектов на карте
    for map_ in maps:
        animated_entities = pygame.sprite.Group()
        entities = pygame.sprite.Group()
        entities_list = []
        platforms = []
        for i in map_:
            if i[0] == 'p':
                pl = Platform(i[1], i[2])
                entities_list.append(pl)
                platforms.append(pl)
            if i[0] == 'e':
                en = Platform(i[1], i[2])
                entities_list.append(en)
            if i[0] == 'c':
                cn = Coin(i[1], 1)
                entities_list.append(cn)
                animated_entities.add(cn)
            if i[0] == 'w':
                wt = Water(i[1], i[2])
                entities_list.append(wt)
                animated_entities.add(wt)
            if i[0] == 'P':
                player_coordinates.append([i[1], i[2]])
        hero = Player(player_coordinates[count_win][0], player_coordinates[count_win][1], 0,
                      total_level_width, total_level_height)
        entities_list.append(hero)
        entities_list.reverse()
        for entity in entities_list:
            entities.add(entity)
        entities_on_maps.append(entities)
        platforms_on_maps.append(platforms)
        animated_entities_on_maps.append(animated_entities)
    while run:
        timer = pygame.time.Clock()
        timer.tick(tick)
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
        # Создаём группу сущностей и список объектов и создаём в ней героя

        if hero.winner:
            count_win += 1
            Size_map = levels[count_win].map_size
            total_level_height, total_level_width = Size_map.height*platform_height, Size_map.width*platform_width
            hero = Player(player_coordinates[count_win][0], player_coordinates[count_win][1], 0,
                          total_level_width, total_level_height)

        frames += 1
        real_time = time.time()
        # частота обновления кадров
        if real_time - new_time > 1:
            new_time = time.time()
            FPS = frames
            if FPS < need_fps:
                tick += 1
            elif FPS > need_fps:
                tick -= 1
            frames = 0

        # обновление анимированных объектов
        if frames % 3 == 0:
            animated_entities_on_maps[count_win].update()
        # Параллакс
        screen.blit(bg, (camera.state.x/2, camera.state.y/2))
        # прорисовка всех объектов
        for entity in entities_on_maps[count_win]:
            screen.blit(entity.image, camera.apply(entity))
            if type(entity) == Coin and distance_is(30, entity, hero):
                coins += 1
                entity.kill()
        # Счётчик монет
        coin_counter(coins, screen)
        fps_counter(FPS, screen)
        # прорисовка главного героя
        camera.update(hero)
        # обновление показаний главного героя
        hero.update(left, right, up, platforms_on_maps[count_win], FPS)
        # обновление экрана
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
