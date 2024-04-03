from modules.cosmos.galaxy_PathFinder import pathFinder
from modules.starter.starter import hero
from modules.game.fight_sim import fight_simulation
from data.planets import tiles_index


def galaxy_gps():
    startPoint = tiles_index.index(next(seq for seq in tiles_index if seq['seq'] == hero["space"]['space_seq']))
    endPoint = tiles_index.index(next(seq for seq in tiles_index if hero["farm_cfg"]['mob_lvl'] in range(seq['mobs'][0], seq['mobs'][1] + 1)))
    pathArr = pathFinder()[startPoint][endPoint]
    path_list = []
    if startPoint == endPoint:
        return 'Done'
    else:
        for path in pathArr['path']:
            path_list.append(tiles_index[path]['seq'])
        print(path_list)
        return path_list


def get_planet_seq(planet_name):
    f_planet = next(planet for planet in tiles_index if planet['name'] == planet_name)
    planet_seq = f_planet['seq']
    return planet_seq


async def mob_emoji():
    cur_planet = next(seq for seq in tiles_index if seq['seq'] == hero["space"]['space_seq'])
    emoji_list = ['🐺', '🐙', '🐍', '🦑']
    search_emoji = []
    all_mobs = list(range(cur_planet['mobs'][0], cur_planet['mobs'][1] + 1))
    if hero['farm_cfg']['any_lvls']:
        for am in all_mobs:
            win_chance = await fight_simulation(optional_mob=am)
            if 'wr' in win_chance and win_chance['wr'] >= 100:
                index = all_mobs.index(am)
                search_emoji.append(emoji_list[index])
    else:
        target_mob = hero["farm_cfg"]['mob_lvl']
        # print(list(range(cur_planet['mobs'][0], cur_planet['mobs'][1] + 1)))
        index = all_mobs.index(target_mob)
        search_emoji.append(emoji_list[index])
    return search_emoji
