from modules.peh.pathsFinder_nebula import pathFinder


def gps(start, end):
    stationNames = ['Альфа', 'Таф', 'Дигамма', 'Кси', 'База', 'Каппа', 'Стигма', 'Вита', 'Дельта', 'Омега', 'Гамма',
                    'Йота', 'Тетта', 'Итта', 'Дзита', 'Эпсилонн']

    # print('one station')
    startPoint = stationNames.index(start)
    endPoint = stationNames.index(end)
    pathArr = pathFinder()[startPoint][endPoint]

    return pathArr
