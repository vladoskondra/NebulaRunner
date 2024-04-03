from modules.starter.starter import hero
import random
import enum
from data.planets import tiles_index
from data.mobs import get_mob


class MIN_DD_CLASS(enum.Enum):
    warrior = 0.05
    ranger = 0.04
    mage = 0.03


async def get_planet_mobs():
    cur_planet = hero['space']['space_seq']
    f_planet = next(planet for planet in tiles_index if planet['seq'] == cur_planet)
    mobs = range(f_planet['mobs'][0], f_planet['mobs'][1] + 1)
    return mobs


async def fight_simulation(optional_mob=0):
    player_obj = {
        'name': 'hero',
        'class': hero['hero']['class'],
        'lvl': hero['hero']['lvl'],
        'hps': hero['hero']['cur_hp'],
        'hpl': hero['hero']['cur_hp'],
        'dmg': hero['hero']['atk'],
        'def': hero['hero']['def'],
        'ddg': hero['hero']['ddg'],
        'crit': hero['hero']['crit'],
        'acc': hero['hero']['acc'],
        'speed': hero['hero']['spd']
    }
    mob_cls = 'any'
    mobs_list = []
    if hero['space']['cosmos']:
        lvls_to_sim = [hero["farm_cfg"]['mob_lvl']]
        if hero['farm_cfg']['any_lvls']:
            lvls_to_sim = await get_planet_mobs()
        for pot_cls in ['warrior', 'ranger', 'mage']:
            if optional_mob == 0:
                for lts in lvls_to_sim:
                    mob = get_mob(lts, cls=pot_cls)
                    mobs_list.append(mob)
            else:
                mob = get_mob(optional_mob, cls=pot_cls)
                mobs_list.append(mob)
    else:
        if hero["farm_cfg"]['mob_cls'] != 'any':
            mob_cls = hero["farm_cfg"]['mob_cls']
        if optional_mob == 0:
            mob = get_mob(hero["farm_cfg"]['mob_lvl'], cls=mob_cls)
        else:
            mob = get_mob(optional_mob, cls=mob_cls)
        mobs_list.append(mob)
    wins_list = []
    ttl_wl = []
    for m in mobs_list:
        enemy_obj = {
            'name': 'mob',
            'class': m['monsterType'].lower(),
            'lvl': m['level'],
            'hps': m['hP'],
            'hpl': m['hP'],
            'dmg': round(m['attack']),
            'def': round(m['def']),
            'ddg': m['dodge'],
            'crit': m['critRate'],
            'acc': m['accuracy'],
            'speed': m['speed']
        }
        wins = {
            player_obj['name']: 0,
            enemy_obj['name']: 0
        }
        loops = 10000
        fight_loop = 0
        while fight_loop < loops:
            fight_text = ''
            first = player_obj
            second = enemy_obj
            if player_obj['speed'] < enemy_obj['speed']:
                first = enemy_obj
                second = player_obj
            elif player_obj['speed'] == enemy_obj['speed']:
                rnd = round(random.uniform(0, 1))
                if rnd == 1:
                    first = enemy_obj
                    second = player_obj
            rounds = 0
            dodges = {
                first['name']: 0,
                second['name']: 0
            }
            while first['hpl'] > 0 and second['hpl'] > 0:
                randomDDG_2 = random.uniform(0, 100)
                if randomDDG_2 <= (second['ddg'] - first['acc']):
                    dodges[second['name']] += 1
                else:
                    randomCRIT_1 = random.uniform(0, 100)
                    if randomCRIT_1 <= first['crit']:
                        DD = round((first['dmg'] - second['def']) * 1.2)
                        minDD = round(second['hps'] * MIN_DD_CLASS[second['class']].value)
                        if DD <= minDD:
                            DD = minDD
                        second['hpl'] = second['hpl'] - DD
                    else:
                        DD = first['dmg'] - second['def']
                        minDD = round(second['hps'] * MIN_DD_CLASS[second['class']].value)
                        if DD <= minDD:
                            DD = minDD
                        second['hpl'] = second['hpl'] - DD
                tmpHero = first
                first = second
                second = tmpHero
                rounds += 1
            fight_loop += 1
            if second['hpl'] < 0:
                wins[first['name']] += 1
            else:
                wins[second['name']] += 1
            first['hpl'] = first['hps']
            second['hpl'] = second['hps']
        winRate = float('{:.2f}'.format((wins['hero'] / fight_loop) * 100))
        if any(mwr['lvl'] == enemy_obj['lvl'] for mwr in wins_list):
            f_m = next(mwr for mwr in wins_list if mwr['lvl'] == enemy_obj['lvl'])
            fmi = wins_list.index(f_m)
            wins_list[fmi]['wr'].append(winRate)
        else:
            wins_list.append({'lvl': enemy_obj['lvl'], 'wr': [winRate]})
    # print(f"wind_list: {wins_list}")
    for wl in wins_list:
        print(f"wl: {wl}")
        if all(w >= 100 for w in wl['wr']):
            ttl_wl.append({'lvl': wl['lvl'], 'wr': 100})

    return max(ttl_wl, key=lambda x:x['lvl'])
