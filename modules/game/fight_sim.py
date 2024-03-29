from modules.starter.starter import hero
import random
import enum
from data.mobs import get_mob


class MIN_DD_CLASS(enum.Enum):
    warrior = 0.05
    ranger = 0.04
    mage = 0.03


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
    if hero["farm_cfg"]['mob_cls'] != 'any':
        mob_cls = hero["farm_cfg"]['mob_cls']
    if optional_mob == 0:
        mob = get_mob(hero["farm_cfg"]['mob_lvl'], cls=mob_cls)
    else:
        mob = get_mob(optional_mob, cls=mob_cls)
    enemy_obj = {
        'name': 'mob',
        'class': mob['monsterType'].lower(),
        'lvl': mob['level'],
        'hps': mob['hP'],
        'hpl': mob['hP'],
        'dmg': round(mob['attack']),
        'def': round(mob['def']),
        'ddg': mob['dodge'],
        'crit': mob['critRate'],
        'acc': mob['accuracy'],
        'speed': mob['speed']
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
    return winRate
