from levels import levels

platform_width = 32
platform_height = 32
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
            if char == '*':
                world_map_new.append([i * platform_width, j * platform_height, 'blockdie'])
            if char == '1':
                world_map_new.append([i * platform_width + 10, j * platform_height, 'blockwin'])
            if char == "=":
                world_map_new.append([i * platform_width, j * platform_height, 'steelblock'])
            if char == "p":
                world_map_new.append([i * platform_width, j * platform_height, 'Player'])
            if char == "W":
                world_map_new.append([i * platform_width, j * platform_height, 'waterfall'])
    return world_map_new


for i in levels:
    maps.append(new_world_map(i))
