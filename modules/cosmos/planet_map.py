from modules.starter.starter import hero
import regex


async def create_planet_map(map_list):
    map_dict = {}
    map_limit = (hero["space"]['planet_size']-1, hero["space"]['planet_size']-1)
    barriers = ['🟦', '🏔', '❄', '❄️', '🟧']
    # print(map_limit)
    for h in range(len(map_list)):
        # print(len(map_list))
        for w in range(len(map_list[h])):
            # print(len(map_list[h]))
            dir_E = None
            dir_W = None
            dir_N = None
            dir_S = None
            dir_NE = None
            dir_NW = None
            dir_SE = None
            dir_SW = None
            # North
            if any(x < y for x, y in zip((h-1, w), (0, 0))):
                dir_N = None
            elif map_list[h-1][w] not in barriers:
                dir_N = (h-1, w)
            # South
            if any(x > y for x, y in zip((h+1, w), map_limit)):
                dir_S = None
            elif map_list[h+1][w] not in barriers:
                dir_S = (h+1, w)
            # West
            if any(x < y for x, y in zip((h, w-1), (0, 0))):
                dir_W = None
            elif map_list[h][w-1] not in barriers:
                dir_W = (h, w-1)
            # East
            if any(x > y for x, y in zip((h, w+1), map_limit)):
                dir_E = None
            elif map_list[h][w+1] not in barriers:
                dir_E = (h, w+1)
            # North-East
            if any(x < y for x, y in zip((h-1, w+1), (0, 0))) or any(x > y for x, y in zip((h-1, w+1), map_limit)):
                dir_NE = None
            elif map_list[h-1][w+1] not in barriers:
                dir_NE = (h-1, w+1)
            # North-West
            if any(x < y for x, y in zip((h-1, w-1), (0, 0))) or any(x > y for x, y in zip((h-1, w-1), map_limit)):
                dir_NW = None
            elif map_list[h-1][w-1] not in barriers:
                dir_NW = (h-1, w-1)
            # South-East
            if any(x < y for x, y in zip((h+1, w+1), (0, 0))) or any(x > y for x, y in zip((h+1, w+1), map_limit)):
                dir_SE = None
            elif map_list[h+1][w+1] not in barriers:
                dir_SE = (h+1, w+1)
            # South-West
            if any(x < y for x, y in zip((h+1, w-1), (0, 0))) or any(x > y for x, y in zip((h+1, w-1), map_limit)):
                dir_SW = None
            elif map_list[h+1][w-1] not in barriers:
                dir_SW = (h+1, w-1)
            map_dict[(h, w)] = {'E': dir_E, 'W': dir_W, 'N': dir_N, 'S': dir_S,
                                'NE': dir_NE, 'NW': dir_NW, 'SE': dir_SE, 'SW': dir_SW}
    # print(map_dict)
    return map_dict


async def make_map_list(text):
    map_list = []
    map_text = text.split('/mapSize /mType /cruiseOn\n\n')[1]
    text_rows = map_text.split('\n')
    for row in text_rows:
        # for l in range(len(row)):
        #     print(row[l])
        emojis = regex.findall(r'\X', row)
        # print(emojis)
        # split_string = row.split()
        # map_row = [i for i in emojis if i in emoji.UNICODE_EMOJI.keys()]
        map_list.append(emojis)
    return map_list