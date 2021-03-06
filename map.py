import pygame

from levels import levels

platform_width = 50
platform_height = 50
platform_color = '#FF6262'
png_height = 18
png_width = 18

rect = pygame.Rect

maps = []


def to_four(string):
    is_four = None
    string = str(string)
    if len(string) < 4:
        is_four = False

    while not is_four:
        string = '0' + string
        if len(string) == 4:
            is_four = True
    return string


def new_world_map(level):
    world_map_new = []
    layers = level.layers
    for layer in layers:
        if layer.name == 'Entities':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char != 0:
                        char -= 1
                        str_char = str(char)
                        str_char = to_four(str_char)
                        image = pygame.image.load(f'tiles/Tiles/tile_{str_char}.png')
                        image = pygame.transform.scale(image, (platform_height, platform_width))
                        world_map_new.append(
                            ["e", rect(platform_height * x, platform_width * y, platform_width, platform_height), image]
                        )
        elif layer.name == 'Platforms and entities':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char != 0:
                        char -= 1
                        str_char = str(char)
                        str_char = to_four(str_char)
                        image = pygame.image.load(f'tiles/Tiles/tile_{str_char}.png')
                        image = pygame.transform.scale(image, (platform_height, platform_width))
                        world_map_new.append(
                            ["p", rect(platform_height * x, platform_width * y, platform_width, platform_height), image]
                        )

        elif layer.name == 'Ladders':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char != 0:
                        char -= 1
                        str_char = str(char)
                        str_char = to_four(str_char)
                        image = pygame.image.load(f'tiles/Tiles/tile_{str_char}.png')
                        image = pygame.transform.scale(image, (platform_height, platform_width))
                        world_map_new.append(
                            ["ld", rect(platform_height * x, platform_width * y, platform_width, platform_height), image]
                        )

        elif layer.name == 'Die_Blocks':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char == 69:
                        world_map_new.append(
                            ["bd", platform_height * x, platform_width * y]
                        )

        elif layer.name == 'Block_win':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char != 0:
                        char -= 1
                        str_char = str(char)
                        str_char = to_four(str_char)
                        image = pygame.image.load(f'tiles/Tiles/tile_{str_char}.png')
                        image = pygame.transform.scale(image, (platform_height, platform_width))
                        world_map_new.append(
                            ["bw", rect(platform_height * x, platform_width * y, platform_width, platform_height), image]
                        )
        elif layer.name == 'Entities_under':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char != 0:
                        char -= 1
                        str_char = str(char)
                        str_char = to_four(str_char)
                        image = pygame.image.load(f'tiles/Tiles/tile_{str_char}.png')
                        image = pygame.transform.scale(image, (platform_height, platform_width))
                        world_map_new.append(
                            ["e_u", rect(platform_height * x, platform_width * y, platform_width, platform_height), image]
                        )
        elif layer.name == 'Entities_under2':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char != 0:
                        char -= 1
                        str_char = str(char)
                        str_char = to_four(str_char)
                        image = pygame.image.load(f'tiles/Tiles/tile_{str_char}.png')
                        image = pygame.transform.scale(image, (platform_height, platform_width))
                        world_map_new.append(
                            ["e_u2", rect(platform_height * x, platform_width * y, platform_width, platform_height), image]
                        )
        elif layer.name == 'Coins':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char == 152:
                        world_map_new.append(
                            ["c", rect(platform_height * x, platform_width * y, platform_width, platform_height)]
                        )
        elif layer.name == 'Water':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char != 0:
                        char -= 1
                        if char == 74:
                            animation = [pygame.transform.scale(
                                    pygame.image.load(f"tiles/Tiles/tile_{(to_four(i))}.png"),
                                    (platform_width, platform_height))
                                for i in range(char, char + 2)
                            ]
                            block = 'wf'
                        elif char == 33 or char == 53:
                            animation = [
                                pygame.transform.scale(
                                    pygame.image.load(f"tiles/Tiles/tile_{(to_four(i))}.png"),
                                    (platform_width, platform_height))
                                for i in [33, 53]
                            ]
                            block = 'w'
                        else:
                            animation = [
                                pygame.transform.scale(
                                    pygame.image.load(f"tiles/Tiles/tile_{(to_four(i))}.png"),
                                    (platform_width, platform_height))
                                for i in range(char, char+2)
                            ]
                            block = 'w'


                        world_map_new.append(
                            [block, rect(platform_height * x, platform_width * y, platform_width, platform_height),
                             animation]
                        )
        elif layer.name == "Player":
            for player in layer.tiled_objects:
                playerX = int(player.coordinates.x*platform_width/png_width)
                playerY = int(player.coordinates.y*platform_height/png_height)
                world_map_new.append(
                    ['P', playerX, playerY]
                )
                print(player)
        elif layer.name == "Moving":
            for obj in layer.tiled_objects:
                id_block = obj.gid - 1
                id_block = to_four(str(id_block))
                image = pygame.image.load(f'tiles/Tiles/tile_{id_block}.png')
                image = pygame.transform.scale(image, (platform_height, platform_width))
                x = obj.coordinates.x*platform_width/png_width
                y = obj.coordinates.y*platform_height/png_height - platform_height
                width = platform_width
                height = platform_height
                tox = obj.properties.get("toX")*platform_width/png_width
                toy = obj.properties.get("toY")*platform_height/png_height - platform_height
                world_map_new.append(
                    ['m', rect(x, y, width, height), image, (tox, toy), 200]
                )
        elif layer.name == 'AlphaEntities':
            for y, row in enumerate(layer.data):
                for x, char in enumerate(row):
                    if char != 0:
                        char -= 1
                        str_char = str(char)
                        str_char = to_four(str_char)
                        image = pygame.image.load(f'tiles/Tiles/tile_{str_char}.png')
                        image = pygame.transform.scale(image, (platform_height, platform_width))
                        world_map_new.append(
                            ["ae",
                             rect(platform_height * x, platform_width * y, platform_width, platform_height),
                             image]
                        )

    return world_map_new


for k in levels:
    maps.append(new_world_map(k))
