import math
import asyncio
from random import randint
from modules.starter.starter import client, hero, const
from modules.cosmos.planet_map import create_planet_map, make_map_list
from modules.utils.dixtra import dijkstra
from modules.cosmos.galaxy_gps import mob_emoji
from modules.cosmos.planet_seek_ship import ship_coord


async def seek_mob(text, target_mob, my_pos):
    while target_mob != my_pos:
        mob_e = await mob_emoji()
        map_list = await make_map_list(text)
        found_mobs = await mobs_coord(map_list)
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
                            ship = await ship_coord(map_list)
                            if not ship or math.dist(target_mob, ship[0]) >= 2:
                                del path[-1]
                            while path:
                                await client.send_message(const['game'], path[0])
                                path.pop(0)
                                await asyncio.sleep(randint(1, 2))
                            if math.dist(target_mob, ship[0]) < 2:
                                possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                                path = []
                                for pd in possible_dirs:
                                    new_pos = tuple(map(lambda i, j: i + j, target_mob, pd))
                                    path = dijkstra(planet_map, target_mob, new_pos)
                                    if path and math.dist(target_mob, new_pos) < 2 and math.dist(target_mob, ship[0]) >= 2:
                                        break
                                await client.send_message(const['game'], path[0])
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
                    isEmoji = False
                    path = []
                    new_msg = ''
                    dir_i = -1
                    while not isEmoji:
                        possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                        path = dijkstra(planet_map, my_pos, tuple(map(lambda i, j: i + j, my_pos, possible_dirs[dir_i])))
                        if not path:
                            dir_i += 1
                        await client.send_message(const['game'], path[0])
                        await asyncio.sleep(1)
                        new_msg = await client.get_messages(const['game'], ids=const['space_map_msg'])
                        if any(emo in new_msg.message for emo in mob_e):
                            isEmoji = True
                        map_list = await make_map_list(new_msg.message)
                        planet_map = await create_planet_map(map_list)
                    found_mobs = await mobs_coord(map_list)
                    nearest_mob = min(found_mobs, key=lambda x: math.dist(x, my_pos))
                    path = dijkstra(planet_map, my_pos, nearest_mob)
                    return ['No path', path]
        else:
            isEmoji = False
            path = []
            new_msg = ''
            dir_i = 0
            while not isEmoji:
                possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                while not path:
                    dir_i += 1
                    path = dijkstra(planet_map, my_pos, tuple(map(lambda i, j: i + j, my_pos, possible_dirs[dir_i])))
                    print(f"{dir_i}: {path}")
                path = dijkstra(planet_map, my_pos, tuple(map(lambda i, j: i + j, my_pos, possible_dirs[dir_i])))
                print(f'Lurking around: {path}')
                if path:
                    await client.send_message(const['game'], path[0])
                await asyncio.sleep(1)
                new_msg = await client.get_messages(const['game'], ids=const['space_map_msg'])
                if any(emo in new_msg.message for emo in mob_e):
                    isEmoji = True
                map_list = await make_map_list(new_msg.message)
                planet_map = await create_planet_map(map_list)
            found_mobs = await mobs_coord(map_list)
            nearest_mob = min(found_mobs, key=lambda x: math.dist(x, my_pos))
            path = dijkstra(planet_map, my_pos, nearest_mob)
            return ['No path', path]


async def mobs_coord(map_list):
    mob_e = await mob_emoji()
    found_mobs = []
    for y in range(len(map_list)):
        for x in range(len(map_list[y])):
            if map_list[y][x] in mob_e:
                found_mobs.append((y, x))
    return found_mobs