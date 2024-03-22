from telethon import events
import asyncio
from modules.starter.starter import client, hero, const
from modules.peh.peh import get_peh_point
from modules.utils.files import update_file


EMOJI_ON = '✅'
EMOJI_OFF = '❌'


@events.register(events.NewMessage(chats='me', from_users='me'))
async def user_handler(event):
    message = event.message.to_dict()
    text = message['message']
    if text.lower() == '.help':
        await client.send_message('me', 'Доступные команды:\n\n'
                                        '**===== РЕЖИМЫ =====**\n'
                                        '• `.farm` — режим обычного гринда мобов\n'
                                        '• `.boost` — режим гринда с банками\n'
                                        '• `.peh` — режим перемещения на ПЕХе (перед включением необходимо долететь до Островов)\n'
                                        '• `.stop` — поставить бота на паузу\n'
                                        '• `.captcha on/off` — включить/выключить автопрохождение капчи\n\n'
                                        '**===== ГРИНД =====**\n'
                                        '• `.mobs LVL CLS` — указать уровень __(LVL)__ и класс __(CLS)__ моба для фарма\n'
                                        '• `.farm_loc LOC` — указать локацию __(LOC)__ для фарма\n(например, `.farm_loc ⛰ Ущелье Дриад`)\n'
                                        '• `.all_mobs on/off` — фармить все возможные уровни мобов на планете\n'
                                        '• `.must_heal on/off` — обязательный отхил у корабля\n\n'
                                        '**===== ПРОФА =====**\n'
                                        '• `.prof RES` — указать через пробел профессию добычи ресурсов __(RES)__: трава, камень, лес, рыба\n'
                                        '• `.prof_rare on/off` — включить/выключить добычу редких событий профы\n'
                                        '• `.multitool on/off` — включить/выключить добычу ресурсов мультитулом\n\n'
                                        '**===== ЭТАПЫ =====**\n'
                                        '• `.edem on/off` — включи, если ты в Эдеме\n'
                                        '• `.cosmos on/off` — включит, если ты в космосе)\n\n'
                                        '**===== КОСМОС =====**\n'
                                        '• `.cosmos_mode` — переключатель режима фарма в космосе')

    if text == '.stop' or text == '.farm' or text == '.dg' or text == '.boost' or text == '.peh':
        hero['mode'] = text.split('.')[1]
        const['orig_msg_status'] = f'Включен режим **{hero["mode"]}**'
        if text.lower() == '.stop':
            const['orig_msg_status'] = f'Бот остановлен'
            hero['state'] = 'none'
            hero['loc'] = 'default'
        const["msg_status"] = await client.send_message('me', const['orig_msg_status'])
        if hero['mode'] in ['farm', 'boost']:
            if hero['space']['cosmos']:
                await client.send_message(const['game'], '🗺 Исследовать')
            if hero['farm_cfg']['farm_loc'] == 'none' and not hero['space']['cosmos']:
                msg_to_del = await client.send_message('me',
                                                       f'Не указана локация для фарма, используй "`.farm_loc` " '
                                                       f'и название, чтоб выставить локацию')
                await asyncio.sleep(60)
                await client.delete_messages('me', msg_to_del)
            if hero['prof_cfg']['prof_loc'] == 'none':
                msg_to_del = await client.send_message('me',
                                                       f'Не указана локация для профы, используй "`.prof_loc` " '
                                                       f'и вид добычи (лес, трава, рыба или камень)')
                await asyncio.sleep(60)
                await client.delete_messages('me', msg_to_del)
            if hero['farm_cfg']['mob_lvl'] == 1 or hero['farm_cfg']['mob_cls'] not in ['warrior', 'ranger', 'mage']:
                msg_to_del = await client.send_message('me',
                                                       f'Не указан моб для фарма! Чтобы указать, используй "`.mobs lvl cls`",'
                                                       f' где __lvl__ — числовой уровень моба, а __cls__ — его класс '
                                                       f'(w - Воин, r - Лучник, m - Маг)')
                await asyncio.sleep(60)
                await client.delete_messages('me', msg_to_del)
    if '.edem ' in text:
        if text == '.edem on':
            hero["general_cfg"]['edem'] = True
            await event.reply(f'{EMOJI_ON} Включен Эдем')
            await reformat_prof_loc()
        elif text == '.edem off':
            hero["general_cfg"]['edem'] = False
            await event.reply(f'{EMOJI_OFF} Выключен Эдем')
            await reformat_prof_loc()
    if '.farm_loc ' in text:
        hero["farm_cfg"]['farm_loc'] = text.split('farm_loc ')[1]
        await event.reply(f'Локация для фарма: **{hero["farm_cfg"]["farm_loc"]}**')
    if '.prof ' in text:
        prof = text.split('prof ')[1]
        hero["prof_cfg"]['prof'] = prof
        await reformat_prof_loc()
        await event.reply(f'Локация для фарма профессии {hero["prof_cfg"]["prof"]}: **{hero["prof_cfg"]["prof_loc"]}**')
    if '.multitool ' in text:
        if text == '.multitool on':
            hero['prof_cfg']['multitool'] = True
            await event.reply(f'{EMOJI_ON} Включен 🔫Мультитул')
        elif text == '.multitool off':
            hero['prof_cfg']['multitool'] = False
            await event.reply(f'{EMOJI_OFF} Выключен 🔫Мультитул')
    if '.prof_rare ' in text:
        if text == '.prof_rare on':
            hero["prof_cfg"]['catch_rare'] = True
            await event.reply(f'{EMOJI_ON} Включена добыча редких событий')
        elif text == '.prof_rare off':
            hero["prof_cfg"]['catch_rare'] = False
            await event.reply(f'{EMOJI_OFF} Выключена добыча редких событий')
    if '.captcha ' in text:
        if text == '.captcha on':
            hero["general_cfg"]['captcha'] = True
            await event.reply(f'{EMOJI_ON} Включен автопроход капчи')
        elif text == '.captcha off':
            hero["general_cfg"]['captcha'] = False
            await event.reply(f'{EMOJI_OFF} Выключен автопроход капчи')
    if '.mobs ' in text:
        if len(text.split(' ')) == 3:
            try:
                mob_lvl = int(text.split(' ')[1])
                mob_cls_raw = text.split(' ')[2]
                if mob_cls_raw in ['w', 'r', 'm']:
                    if mob_cls_raw == 'w':
                        hero["farm_cfg"]['mob_cls'] = 'warrior'
                    elif mob_cls_raw == 'r':
                        hero["farm_cfg"]['mob_cls'] = 'ranger'
                    elif mob_cls_raw == 'm':
                        hero["farm_cfg"]['mob_cls'] = 'mage'
                    hero["farm_cfg"]['mob_lvl'] = mob_lvl
                    await event.reply(f'Выбран {mob_lvl} уровень моба для фарма')
                else:
                    await event.reply(f'Неверно указан класс моба. Используй команду "`.mobs {mob_lvl} cls`", '
                                      f'где __cls__ — класс моба (w - Воин, r - Лучник, m - Маг)')
            except:
                await event.reply('Неправильно указан уровень моба для фарма.\n'
                                  'Используй команду "`.mobs lvl`" или "`.mobs lvl cls`", '
                                  'где __lvl__ — уровень моба для фарма, '
                                  'а __cls__ — класс моба (w - Воин, r - Лучник, m - Маг)')
        else:
            await event.reply('Неправильно указан уровень моба для фарма.\n'
                              'Используй команду "`.mobs lvl`" или "`.mobs lvl cls`", '
                              'где __lvl__ — уровень моба для фарма, '
                              'а __cls__ — класс моба (w - Воин, r - Лучник, m - Маг)')
    if '.cosmos ' in text:
        if text == '.cosmos on':
            hero["space"]['cosmos'] = True
            await event.reply(f'{EMOJI_ON} Включен космос')
            await reformat_prof_loc()
        elif text == '.cosmos off':
            hero["space"]['cosmos'] = False
            await event.reply(f'{EMOJI_OFF} Выключен космос')
            await reformat_prof_loc()
    if text.lower() == '.cosmos_mode':
        if hero["space"]['cosmos_farm_seek']:
            hero["space"]['cosmos_farm_seek'] = False
            await event.reply('Режим фарма в космосе: **Ожидание воскрешения моба**')
        else:
            hero["space"]['cosmos_farm_seek'] = True
            await event.reply('Режим фарма в космосе: **Бег между живыми мобами**')
    if '.must_heal ' in text:
        if text == '.must_heal on':
            hero["farm_cfg"]['force_heal'] = True
            await event.reply(f'{EMOJI_ON} Включен обязательный отхил')
        elif text == '.must_heal off':
            hero["farm_cfg"]['force_heal'] = False
            await event.reply(f'{EMOJI_OFF} Выключен обязательный отхил')
    if '.all_mobs ' in text:
        if text == '.all_mobs on':
            hero["farm_cfg"]['any_lvls'] = True
            await event.reply(f'{EMOJI_ON} Включен обязательный отхил')
        elif text == '.all_mobs off':
            hero["farm_cfg"]['any_lvls'] = False
            await event.reply(f'{EMOJI_OFF} Выключен обязательный отхил')
    if text.startswith('⚔️ '):
        pin = text.split('\n')[0].split(' ')[1]
        point = await get_peh_point(pin.lower())
        print(point)
    update_file('hero', hero)


async def reformat_prof_loc():
    prof = hero["prof_cfg"]['prof']
    if prof == 'рыба':
        if hero["space"]['cosmos']:
            hero["prof_cfg"]['prof_loc'] = '🍤'
        elif not hero["general_cfg"]['edem']:
            hero["prof_cfg"]['prof_loc'] = '🏝 Побережье Карха'
        else:
            hero["prof_cfg"]['prof_loc'] = '🌉 Дистрикт Вайресс'
    elif prof == 'лес' or prof == 'трава':
        if hero["space"]['cosmos']:
            if prof == 'лес':
                hero["prof_cfg"]['prof_loc'] = '🌴'
            elif prof == 'трава':
                hero["prof_cfg"]['prof_loc'] = '🍃'
        elif not hero["general_cfg"]['edem']:
            hero["prof_cfg"]['prof_loc'] = '🌳 Лес Предтеч'
        else:
            if prof == 'лес':
                hero["prof_cfg"]['prof_loc'] = '🌃 Дистрикт Аппалачи'
            elif prof == 'трава':
                hero["prof_cfg"]['prof_loc'] = '🌇 Дистрикт Древних'
    elif prof == 'камень':
        if hero["space"]['cosmos']:
            hero["prof_cfg"]['prof_loc'] = '🗿'
        elif not hero["general_cfg"]['edem']:
            hero["prof_cfg"]['prof_loc'] = '🧊 Кварцевое Плато'
        else:
            hero["prof_cfg"]['prof_loc'] = '🌃 Дистрикт Аппалачи'