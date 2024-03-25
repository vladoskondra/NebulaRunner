# from turtle import distance
import math
import asyncio
from random import randint
from modules.starter.starter import client, const, hero
from modules.cosmos.planet_map import create_planet_map, make_map_list
from modules.utils.dixtra import dijkstra
from modules.utils.script_tools import flatten_extend
import re


async def seek_ship(text, target_mob, my_pos):
    print('inside seek_ship')
    while target_mob != my_pos:
        print(f'target != my_pos ({target_mob} | {my_pos})')
        ship_emoji = '🚀'
        map_list = await make_map_list(text)
        # print(map_list)
        planet_map = await create_planet_map(map_list)
        if any(ml == ship_emoji for ml in flatten_extend(map_list)):
            found_ship = await ship_coord(map_list)
            nearest_mob = min(found_ship, key=lambda x: math.dist(x, my_pos))
            print(f'nearest_mob: {nearest_mob}')
            # input('Go?')
            target_mob = nearest_mob
            if target_mob == my_pos:
                return target_mob
            else:
                path = dijkstra(planet_map, my_pos, target_mob)
                isPathFounded = False
                isNoPaths = False
                while not isPathFounded:
                    if path:
                        if len(path) == 1:
                            target_mob = my_pos
                            isPathFounded = True
                        else:
                            del path[-1]
                            while path:
                                await client.send_message(const['game'], path[0])
                                path.pop(0)
                                await asyncio.sleep(randint(1, 2))
                            target_mob = my_pos
                            isPathFounded = True

                    else:
                        while not path:
                            found_ship.pop(found_ship.index(target_mob))
                            if found_ship:
                                target_mob = min(found_ship, key=lambda x: math.dist(x, my_pos))
                                path = dijkstra(planet_map, my_pos, target_mob)
                            else:
                                break
                        isPathFounded = True
                if isPathFounded and not isNoPaths:
                    return target_mob
                elif isNoPaths:
                    i = -1
                    while not path:
                        i += 1
                        possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                        path = dijkstra(planet_map, my_pos, tuple(map(lambda i, j: i + j, my_pos, possible_dirs[i])))
                    return ['No path', path]
        else:
            print('ship is not on map')
            dir = re.sub(r'[0-9]', '', text.split('  🚀: ')[1].split('\n')[0])
            empty_emoji = '⬛'
            max_coord = hero["space"]['planet_size'] - 1
            nearest_mob = (0, 0)
            print(map_list)
            # found_ship = [(i, map_list.index(empty_emoji)) for i, map_list in enumerate(map_list) if empty_emoji in map_list]
            found_ship = await ship_coord(map_list)
            print(found_ship)
            search_coord = (0, 0)
            if dir == '↖️':
                search_coord = (0, 0)
            elif dir == '⬆️':
                search_coord = (0, max_coord/2)
            elif dir == '↗️':
                search_coord = (0, max_coord)
            elif dir == '⬅️':
                search_coord = (max_coord/2, 0)
            elif dir == '➡️':
                search_coord = (max_coord/2, max_coord)
            elif dir == '↙️':
                search_coord = (max_coord, 0)
            elif dir == '⬇️':
                search_coord = (max_coord, max_coord/2)
            elif dir == '↘️':
                search_coord = (max_coord, max_coord)
            # print(search_coord)
            nearest_mob = min(found_ship, key=lambda x: math.dist(x, search_coord))
            # min_dif, res = 999999999, None
            # for i, val in enumerate(found_ship):
            #     dif = abs(search_coord[0] - val[0]) + abs(search_coord[1] - val[1])
            #     if dif < min_dif:
            #         min_dif, res = dif, i
            # nearest_mob = found_ship[res]
            path = dijkstra(planet_map, my_pos, nearest_mob)
            if path:
                print(f"Path from {my_pos} to {nearest_mob}:\n{path}")
                while path:
                    await client.send_message(const['game'], path[0])
                    path.pop(0)
                    await asyncio.sleep(randint(1, 2))
                    # print(f'walked {path[0]}')
            else:
                while not path:
                    found_ship.pop(found_ship.index(nearest_mob))
                    nearest_mob = min(found_ship, key=lambda x: math.dist(x, search_coord))
                    path = dijkstra(planet_map, my_pos, nearest_mob)
                while path:
                    await client.send_message(const['game'], path[0])
                    path.pop(0)
                    await asyncio.sleep(randint(1, 2))
            # input('?')
            return target_mob


async def ship_coord(map_list):
    ship_emoji = '🚀'
    found_ship = []
    for y in range(len(map_list)):
        for x in range(len(map_list[y])):
            if map_list[y][x] == ship_emoji:
                found_ship.append((y, x))
    print(f'Ship at pos: {found_ship}')
    return found_ship
