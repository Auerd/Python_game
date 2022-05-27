import pygame
from pygame import mixer
from levels import levels
from map import maps, platform_width, platform_height
from player import Player, distance
from blocks import Platform, Water, BlockWin, BlockDie, Ladder, AlphaEntity
import Camera as c
import time
from monster import Coin, MovingObject
from counter import coin_counter, fps_counter, lifes_counter
from sounds import set_waterfall_volume

# Высота
win_width = 192 * 8
win_height = 108 * 8
display = (win_width, win_height)  # Дисплей

background_color = '#004400'


def main():
    # Частота кадров которую мы хотим
    need_fps = 60
    # Определяем карту
    Size_map = levels[0].map_size
    total_level_height, total_level_width = Size_map.height * platform_height, Size_map.width * platform_width
    # Инициализация пайгейм
    left = right = up = False
    run = True
    pygame.init()
    # Шрифт
    game_over_font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 50)
    game_over_text = game_over_font.render("GAME OVER", True, (100, 100, 100))
    text_height = game_over_text.get_height()
    text_width = game_over_text.get_width()
    text_x = (win_width - text_width) / 2
    text_y = (win_height - text_height) / 2
    # Инициализация mixer
    mixer.init(channels=1)
    # Звуки
    woods_sound = mixer.Sound("sound/0074.mp3")
    waterfall_sound = mixer.Sound("sound/0052.mp3")
    volume_percent = 30
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
    bg = pygame.transform.scale(bg, (int(bg.get_width() * prop), int(bg.get_height() * prop)))
    # Счётчики
    count_win = 0
    frames = 0
    new_time = time.time()
    FPS = 180
    tick = 80
    coins = 0
    # Списки объектов
    entities_on_maps = []
    platforms_on_maps = []
    animated_entities_on_maps = []
    players_maps = []
    waterfalls_on_maps = []
    woods_sound.play(loops=-1)
    waterfall_sound.play(loops=-1)
    map_counter = 0
    # Переключатель между картами + иницализация объектов на карте
    for map_ in maps:
        animated_entities = pygame.sprite.Group()
        entities = pygame.sprite.Group()
        entities_list = []
        platforms = []
        waterfalls = []
        Size_map = levels[map_counter].map_size
        total_level_height, total_level_width = Size_map.height * platform_height, Size_map.width * platform_width
        for i in map_:
            if i[0] == 'w':
                for num_pic in range(len(i[2])):
                    i[2][num_pic] = i[2][num_pic].convert_alpha()
                wt = Water(i[1], i[2])
                entities_list.append(wt)
                animated_entities.add(wt)
            elif i[0] == 'wf':
                for num_pic in range(len(i[2])):
                    i[2][num_pic] = i[2][num_pic].convert_alpha()
                wf = Water(i[1], i[2])
                entities_list.append(wf)
                animated_entities.add(wf)
                waterfalls.append(wf)
            elif i[0] == 'm':
                mv = MovingObject(i[1], i[2], i[3], i[4])
                entities_list.append(mv)
                animated_entities.add(mv)
                platforms.append(mv)
            elif i[0] == 'bw':
                pl = BlockWin(i[1], i[2])
                entities_list.append(pl)
            elif i[0] == 'ae':
                ae = AlphaEntity(i[1], i[2])
                entities_list.append(ae)
                animated_entities.add(ae)
        for i in map_:
            if i[0] == 'e':
                en = Platform(i[1], i[2])
                entities_list.append(en)
        for i in map_:
            if i[0] == 'c':
                cn = Coin(i[1], 1)
                entities_list.append(cn)
                animated_entities.add(cn)
        for i in map_:
            if i[0] == 'P':
                player_coordinates = [i[1], i[2]]
                hero = Player(player_coordinates[0], player_coordinates[1], 0,
                              total_level_width, total_level_height)
                entities_list.append(hero)
                players_maps.append(hero)
        for i in map_:
            if i[0] == 'p':
                pl = Platform(i[1], i[2])
                entities_list.append(pl)
                platforms.append(pl)
            elif i[0] == 'bd':
                bd = BlockDie(i[1], i[2]+platform_height/2)
                platforms.append(bd)
                bd = BlockDie(i[1], i[2])
                entities_list.append(bd)
        for i in map_:
            if i[0] == 'e_u':
                en = Platform(i[1], i[2])
                entities_list.append(en)
            if i[0] == 'ld':
                ld = Ladder(i[1], i[2])
                entities_list.append(ld)
        for i in map_:
            if i[0] == 'e_u2':
                en = Platform(i[1], i[2])
                entities_list.append(en)
        entities_list.reverse()
        for entity in entities_list:
            entities.add(entity)
        waterfalls_on_maps.append(waterfalls)
        entities_on_maps.append(entities)
        platforms_on_maps.append(platforms)
        animated_entities_on_maps.append(animated_entities)
        map_counter += 1
    # сам цикл
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

        if players_maps[count_win].winner:
            count_win += 1
            Size_map = levels[count_win].map_size
            total_level_height, total_level_width = Size_map.height * platform_height, Size_map.width * platform_width
            camera = c.Camera(total_level_width, total_level_height, win_width, win_height)

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
        screen.blit(bg, (camera.state.x / 2, camera.state.y / 2))
        # прорисовка всех объектов
        for entity in entities_on_maps[count_win]:
            screen.blit(entity.image, camera.apply(entity))
            if type(entity) == Coin and 30 > distance(entity, players_maps[count_win]):
                coins += 1
                entity.kill()
            elif type(entity) == BlockWin and 30 > distance(entity, players_maps[count_win]):
                players_maps[count_win].winner = True
        # Звук
        if len(waterfalls_on_maps[count_win]) > 0:
            waterfall_volume = set_waterfall_volume(
                waterfalls_on_maps[count_win][0], players_maps[count_win], 550
            ) / 100 * volume_percent
            waterfall_sound.set_volume(waterfall_volume)
        else:
            waterfall_sound.set_volume(0)
        woods_volume = volume_percent / 100
        woods_sound.set_volume(woods_volume)
        if players_maps[count_win].lifes < 1:
            screen.fill((0, 0, 0))
            screen.blit(game_over_text, (text_x, text_y))
            volume_percent -= 0.1
            if volume_percent < -10:
                run = False
        # Счётчики
        coin_counter(coins, screen)
        fps_counter(FPS, screen)
        lifes_counter(players_maps[count_win].lifes, screen)
        # обновление положения камеры
        camera.update(players_maps[count_win])
        # обновление показаний главного героя
        players_maps[count_win].update(left, right, up, platforms_on_maps[count_win], FPS, entities_on_maps[count_win])
        # обновление экрана
        pygame.display.update()
    pygame.quit()
    mixer.quit()


if __name__ == '__main__':
    main()
