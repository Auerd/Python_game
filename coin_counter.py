import pygame
from map import platform_width, platform_height

number_png = [pygame.transform.scale(pygame.image.load(f'tiles/Tiles/tile_017{i}.png'),
                                     (platform_width, platform_height))
              for i in range(0, 10)]
png_to_coin = {}
for i in range(len(number_png)):
    png_to_coin.update({str(i): number_png[i]})
print(png_to_coin)


def coin_counter(coins, screen):
    coins = list(str(coins))
    for i in range(len(coins)):
        screen.blit(png_to_coin.get(coins[i]), (platform_width*i/2, int(platform_height*1.5)))
