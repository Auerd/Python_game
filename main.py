import pygame
from map import maps
from map import total_level_height, total_level_width
from player import Player
from blocks import Platform, BlockDie, BlockWin, Steelblock, BlockWaterFall
import Camera as c
import time

win_width = c.win_width  # Ширина
win_height = c.win_height  # Высота
display = (win_width, win_height)  # Дисплей

background_color = '#004400'


def main():
    # Определяем игрока
    hero = Player(55, 55, 0)
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
    camera = c.Camera(c.camera_configure, total_level_width, total_level_height)
    # Карты
    bg = pygame.image.load('bg/maxresdefault.jpg')
    bg = pygame.transform.scale(bg, (int(bg.get_width()/1.1), int(bg.get_height()/1.1)))
    real_count_win = 1
    frame_now = 0
    max_frames = 6
    new_time = time.time()
    while run:
        timer = pygame.time.Clock()
        timer.tick(120)
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
        entities = pygame.sprite.Group()
        platforms = []
        entities.add(hero)

        # Переключатель между картами + иницализация недвижимых объектов на карте
        for i in maps[0]:
            if i[2] == 'platform':
                pf = Platform(i[0], i[1])
                entities.add(pf)
                platforms.append(pf)
            elif i[2] == 'blockwin':
                bw = BlockWin(i[0], i[1])
                entities.add(bw)
                platforms.append(bw)
            elif i[2] == 'blockdie':
                bd = BlockDie(i[0], i[1])
                entities.add(bd)
                platforms.append(bd)
            elif i[2] == 'steelblock':
                sb = Steelblock(i[0], i[1])
                entities.add(sb)
                platforms.append(sb)

        # ненавижу анимации!!! С этой хернёй провозился целый вечер и ничего не получилось. Ненавижу библиотеки! АААААА!
        # сделал вот такой простенький счётчик
        real_time = time.time()
        # частота обновления кадров
        if real_time - new_time > 0.1:
            new_time = time.time()
            frame_now += 1
        # чтобы не выходил за границы массива
        if frame_now == max_frames:
            frame_now = 0

        # Параллакс
        screen.blit(bg, ((camera.state.x - bg.get_width()/2)/2, 0))
        # прорисовка всех объектов
        for entity in entities:
            screen.blit(entity.image, camera.apply(entity))
        # обновление показаний главного героя
        hero.update(left, right, up, platforms)
        # прорисовка главного героя
        camera.update(hero)
        # обновление экрана
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
