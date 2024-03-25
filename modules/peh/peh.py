from telethon import events
import asyncio
from random import randint
from modules.peh.gps import *
from modules.starter.starter import client, hero, const


async def get_peh_point(text):
    if text in ["альфа", "аль"]:
        point_name = 'Альфа'
    elif text in ['таф']:
        point_name = 'Таф'
    elif text in ['диг', "дигама", "дигамма"]:
        point_name = 'Дигамма'
    elif text in ['кси']:
        point_name = 'Кси'
    elif text in ["б", 'база']:
        point_name = 'База'
    elif text in ["к", 'кап', "капа", "каапа", "каппа"]:
        point_name = 'Каппа'
    elif text in ['стиг', "стигма"]:
        point_name = 'Стигма'
    elif text in ['ви', "вита"]:
        point_name = 'Вита'
    elif text in ['дель', "дельт", "дельта"]:
        point_name = 'Дельта'
    elif text in ['ом', "омег", "омега"]:
        point_name = 'Омега'
    elif text in ['гам', "гама", "гамма"]:
        point_name = 'Гамма'
    elif text in ['йо', "йот", "йота"]:
        point_name = 'Йота'
    elif text in ['тет', "тета", "тетта"]:
        point_name = 'Тетта'
    elif text in ['ит', "ита", "итта"]:
        point_name = 'Итта'
    elif text in ['дз', "дзи", "дзит", "дзита"]:
        point_name = 'Дзита'
    elif text in ['э', "эпс", "эпси", "эпсилон", "эпсилонн"]:
        point_name = 'Эпсилонн'
    else:
        point_name = 'ERROR'
    return point_name


@events.register(events.NewMessage(from_users='NebulaHelperBot'))
async def peh_handler(event):
    if hero['mode'] == 'peh':
        message = event.message.to_dict()
        text = message['message']
        if text.startswith('⚔️ '):
            pin = text.split('\n')[0].split(' ')[1]
            const["pin_point"] = await get_peh_point(pin.lower())
            await update_peh_list()


async def update_peh_list():
    const["peh_list"] = []
    station_names = ['Альфа', 'Таф', 'Дигамма', 'Кси', 'База', 'Каппа', 'Стигма', 'Вита', 'Дельта', 'Омега', 'Гамма',
                     'Йота', 'Тетта', 'Итта', 'Дзита', 'Эпсилонн']
    if const["pin_point"] != 'ERROR' and const["pin_point"] != '':
        gps_track = gps(hero['loc'], const["pin_point"])
        for p in range(len(gps_track["path"])):
            if p != 0:
                print(station_names[gps_track["path"][p]])
                if station_names[gps_track["path"][p]] == 'База':
                    const["peh_list"].append('🏛 База Дроидов')
                else:
                    const["peh_list"].append(station_names[gps_track["path"][p]])
        if const["peh_list"] and hero['state'] == 'alive':
            await client.send_message(const['game'], const["peh_list"][0])
            const["peh_list"].pop(0)


async def peh_runner(text):
    if 'К сожалению' in text:
        hero['state'] = 'dead'
    if 'Вы воскрешены' in text:
        hero['state'] = 'alive'
    if 'Вы прибыли на локацию "Острова Грёз"' in text:
        hero['loc'] = 'База'
        hero['state'] = 'alive'
        await client.send_message(const["game"], '🛠 Техосмотр')
        await asyncio.sleep(randint(5, 10))
        await update_peh_list()
    if '🚩 Вы прибыли в локацию: ' in text:
        hero['state'] = 'alive'
        hero['loc'] = text.split('локацию: ')[1].split('.')[0].split(' ')[1]
        if hero['loc'] == 'База':
            await asyncio.sleep(1)
            await client.send_message(const["game"], '🛠 Техосмотр')
        await asyncio.sleep(1)
        if const["peh_list"]:
            await client.send_message(const["game"], const["peh_list"][0])
            const["peh_list"].pop(0)
