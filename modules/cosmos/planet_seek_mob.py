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
        # print(map_list)
        target_mob = await find_path(map_list, target_mob, my_pos, mob_e)
        return target_mob


async def find_path(map_list, target_mob, my_pos, mob_e):
    planet_map = await create_planet_map(map_list)
    found_prof = await mobs_coord(map_list)
    target_mob = min(found_prof, key=lambda x: math.dist(x, my_pos))
    while hero['state'] == 'map seeker':
        if my_pos == target_mob:
            return target_mob
        else:
            path = dijkstra(planet_map, my_pos, target_mob)
            print('Found path after lurking')
            if path:
                # target_mob = await find_path(map_list, path, target_mob, my_pos)
                # if not ship or math.dist(target_mob, ship[0]) >= 2.5:
                #     del path[-1]
                while path:
                    await client.send_message(const['game'], path[0])
                    path.pop(0)
                    await asyncio.sleep(randint(1, 2))
                new_msg = await client.get_messages(const['game'], ids=const['space_map_msg'])
                map_list = await make_map_list(new_msg.message)
                ship = await ship_coord(map_list)
                if ship and math.dist(target_mob, ship[0]) < 2.5:
                    possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                    path = []
                    for pd in possible_dirs:
                        new_pos = tuple(map(lambda i, j: i + j, target_mob, pd))
                        planet_map = await create_planet_map(map_list)
                        path = dijkstra(planet_map, target_mob, new_pos)
                        if path and math.dist(target_mob, new_pos) < 2.5 and math.dist(target_mob, ship[0]) > 2.5:
                            break
                    await client.send_message(const['game'], path[0])
                    await asyncio.sleep(randint(1, 2))
                await asyncio.sleep(1)
                new_msg = await client.get_messages(const['game'], ids=const['space_map_msg'])
                map_list = await make_map_list(new_msg.message)
                mob_e = await mob_emoji()
                isMobExist = []
                for yy in range(-1, 2):
                    for xx in range(-1, 2):
                        isMobExist.append(map_list[int(my_pos[0]) + yy][int(my_pos[1]) + xx])
                if any(m in mob_e for m in isMobExist):
                    target_mob = my_pos
                    return target_mob
                else:
                    target_mob = await seek_mob(new_msg.message, (math.inf, math.inf), my_pos)
                    return target_mob
            else:
                map_list = await lurking(planet_map, my_pos, mob_e)
                target_mob = await find_path(map_list, target_mob, my_pos, mob_e)
                return target_mob


async def lurking(planet_map, my_pos, mob_e):
    isEmoji = False
    path = []
    new_msg = ''
    dir_i = 0
    map_list = []
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
    return map_list


async def mobs_coord(map_list):
    mob_e = await mob_emoji()
    found_mobs = []
    for y in range(len(map_list)):
        for x in range(len(map_list[y])):
            if map_list[y][x] in mob_e:
                found_mobs.append((y, x))
    return found_mobs
