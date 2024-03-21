# from turtle import distance
import math
import asyncio
from random import randint
from modules.starter.starter import client, hero, const
from modules.cosmos.planet_map import create_planet_map
from modules.utils.dixtra import dijkstra
from modules.cosmos.galaxy_gps import mob_emoji


async def seek_prof(text, target_mob, my_pos):
    while target_mob != my_pos:
        prof_e = hero["prof_cfg"]['prof_loc']
        map_list = []
        map_text = text.split('/mapSize /mType /cruiseOn\n\n')[1]
        text_rows = map_text.split('\n')
        for row in text_rows:
            map_row = [i for i in [*row] if i != '️']
            map_list.append(map_row)
        found_mobs = []
        for y in range(len(map_list)):
            for x in range(len(map_list[y])):
                if map_list[y][x] == prof_e:
                    found_mobs.append((y, x))
        planet_map = await create_planet_map(map_list)
        print(f'All mobs: {found_mobs}')
        if found_mobs:
            nearest_mob = min(found_mobs, key=lambda x: math.dist(x, my_pos))
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
                            found_mobs.pop(found_mobs.index(target_mob))
                            if found_mobs:
                                target_mob = min(found_mobs, key=lambda x: math.dist(x, my_pos))
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
            isEmoji = False
            path = []
            new_msg = ''
            while not isEmoji:
                path = []
                i = -1
                while not path:
                    i += 1
                    possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                    path = dijkstra(planet_map, my_pos, tuple(map(lambda i, j: i + j, my_pos, possible_dirs[i])))
                await client.send_message(const['game'], path[0])
                await asyncio.sleep(1)
                new_msg = await client.get_messages(const['game'], ids=const['space_map_msg'])
                if prof_e in new_msg.message:
                    isEmoji = True
            map_text = new_msg.message.split('/mapSize /mType /cruiseOn\n\n')[1]
            text_rows = map_text.split('\n')
            for row in text_rows:
                map_row = [i for i in [*row] if i != '️']
                map_list.append(map_row)
            planet_map = await create_planet_map(map_list)
            found_mobs = []
            for y in range(len(map_list)):
                for x in range(len(map_list[y])):
                    if map_list[y][x] == prof_e:
                        found_mobs.append((y, x))
            nearest_mob = min(found_mobs, key=lambda x: math.dist(x, my_pos))
            path = dijkstra(planet_map, my_pos, nearest_mob)
            return ['No path', path]
