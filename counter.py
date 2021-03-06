import pygame
from map import platform_width, platform_height

number_png = [pygame.transform.scale(pygame.image.load(f'tiles/Tiles/tile_017{i}.png'),
                                     (platform_width, platform_height))
              for i in range(0, 10)]
number_png_small = [pygame.transform.scale(pygame.image.load(f'tiles/Tiles/tile_016{i}.png'),
                                           (platform_width//2, platform_height//2))
                    for i in range(0, 10)]
hearts_png = [pygame.transform.scale(pygame.image.load(f'tiles/Tiles/tile_004{i}.png'),
                                 (platform_width, platform_height))
          for i in range(4, 7)]
hearts_png.reverse()
png_to_coin = {}
for i in range(len(number_png)):
    png_to_coin.update({str(i): number_png[i]})

png_to_fps = {}
for i in range(len(number_png_small)):
    png_to_fps.update({str(i): number_png_small[i]})


def coin_counter(coins, screen):
    coins = list(str(coins))
    for i in range(len(coins)):
        screen.blit(png_to_coin.get(coins[i]), (platform_width*i/2, int(platform_height*1.5)))


def fps_counter(fps, screen):
    fps = list(str(fps))
    fps.reverse()
    for i in range(len(fps)):
        screen.blit(png_to_fps.get(fps[i]), (screen.get_width()-(platform_width*i/4)-50, int(platform_height*1.5)))


def lifes_counter(lifes, screen):
    hearts = []
    if lifes > 0:
        for i in range(lifes//2):
            hearts.append(2)
        if lifes % 2 != 0:
            hearts.append(lifes % 2)
    while len(hearts) < 3:
        hearts.append(0)
    for heart in range(len(hearts)):
        screen.blit(hearts_png[hearts[heart]], (screen.get_width()/2+platform_width*heart-platform_width*3//2,
                                                platform_height))
