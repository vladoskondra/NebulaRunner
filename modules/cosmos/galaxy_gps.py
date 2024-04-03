from modules.cosmos.galaxy_PathFinder import pathFinder
from modules.starter.starter import hero
from modules.game.fight_sim import fight_simulation

tiles_index = [
    {'seq': 'A0', 'name': 'Орион', 'mobs': [1, 30]}, {'seq': 'A1', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'A2', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'A3', 'name': 'Кеплер-4', 'mobs': [-1, -1]}, {'seq': 'A4', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'A5', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'A6', 'name': '', 'mobs': [-1, -1]}, {'seq': 'B1', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'B2', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'B3', 'name': '', 'mobs': [-1, -1]}, {'seq': 'B4', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'B5', 'name': 'Атлон', 'mobs': [31, 33]},
    {'seq': 'B6', 'name': '', 'mobs': [-1, -1]}, {'seq': 'B7', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'B8', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C1', 'name': '', 'mobs': [-1, -1]}, {'seq': 'C2', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C3', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C4', 'name': '', 'mobs': [-1, -1]}, {'seq': 'C5', 'name': 'Таурус', 'mobs': [33, 36]},
    {'seq': 'C6', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C7', 'name': '', 'mobs': [-1, -1]}, {'seq': 'C8', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C9', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C10', 'name': '', 'mobs': [-1, -1]}, {'seq': 'C11', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C12', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C13', 'name': '', 'mobs': [-1, -1]}, {'seq': 'C14', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C15', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'C16', 'name': '', 'mobs': [-1, -1]}, {'seq': 'D1', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D2', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D3', 'name': '', 'mobs': [-1, -1]}, {'seq': 'D4', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D5', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D6', 'name': '', 'mobs': [-1, -1]}, {'seq': 'D7', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D8', 'name': 'Кассиопея', 'mobs': [36, 38]},
    {'seq': 'D9', 'name': '', 'mobs': [-1, -1]}, {'seq': 'D10', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D11', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D12', 'name': '', 'mobs': [-1, -1]}, {'seq': 'D13', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D14', 'name': 'Пиреис', 'mobs': [38, 40]},
    {'seq': 'D15', 'name': '', 'mobs': [-1, -1]}, {'seq': 'D16', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D17', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'D18', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E1', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E2', 'name': 'Хот', 'mobs': [42, 44]},
    {'seq': 'E3', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E4', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E5', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E6', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E7', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E8', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E9', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E10', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E11', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E12', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E13', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E14', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E15', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E16', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E17', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E18', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E19', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E20', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E21', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E22', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E23', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E24', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E25', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E26', 'name': 'Хорвус', 'mobs': [40, 42]},
    {'seq': 'E27', 'name': '', 'mobs': [-1, -1]}, {'seq': 'E28', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E29', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'E30', 'name': '', 'mobs': [-1, -1]}, {'seq': 'F1', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'F2', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'F3', 'name': '', 'mobs': [-1, -1]}, {'seq': 'F4', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'F5', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'F6', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G1', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G2', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G3', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G4', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G5', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G6', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G7', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G8', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G9', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G10', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G11', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G12', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G13', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G14', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G15', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G16', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G17', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G18', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G19', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G20', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G21', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G22', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G23', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G24', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G25', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G26', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G27', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G28', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G29', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G30', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G31', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G32', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G33', 'name': '', 'mobs': [-1, -1]}, {'seq': 'G34', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G35', 'name': '', 'mobs': [-1, -1]},
    {'seq': 'G36', 'name': '', 'mobs': [-1, -1]}]


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


async def get_planet_mobs():
    cur_planet = hero['space']['space_seq']
    f_planet = next(planet for planet in tiles_index if planet['seq'] == cur_planet)
    mobs = range(f_planet['mobs'][0], f_planet[1] + 1)
    return mobs


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
