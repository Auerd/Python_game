from levels import levels
import random

platform_width = 50
platform_height = 50
platform_color = '#FF6262'

total_level_width = len(levels[0][0]) * platform_width
total_level_height = len(levels[0]) * platform_height

maps = []


def new_world_map(level__):
    world_map_new = []
    for j, row in enumerate(level__):
        for i, char in enumerate(row):
            if char == '-':
                world_map_new.append([i * platform_width, j * platform_height, 'platform'])
            elif char == '*':
                world_map_new.append([i * platform_width, j * platform_height, 'blockdie',
                                      j * platform_height + platform_height/2])
            elif char == '1':
                world_map_new.append([i * platform_width + 10, j * platform_height, 'blockwin'])
            elif char == "#":
                world_map_new.append([i * platform_width, j * platform_height, 'steelblock'])
            elif char == "p":
                world_map_new.append([i * platform_width, j * platform_height, 'Player'])
            elif char == "<":
                world_map_new.append([i * platform_width, j * platform_height, 'platform_l'])
            elif char == ">":
                world_map_new.append([i * platform_width, j * platform_height, 'platform_r'])
            elif char == "=":
                world_map_new.append([i * platform_width, j * platform_height, 'platform_m'])
            elif char == "W":
                world_map_new.append([i * platform_width, j * platform_height, char])
            elif char == "C":
                world_map_new.append([i * platform_width, j * platform_height, char])
    return world_map_new


for i in levels:
    maps.append(new_world_map(i))
