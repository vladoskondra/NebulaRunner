from modules.starter.starter import config
from modules.me_handler import *
from modules.game_handler import *
from modules.peh.peh import peh_handler
from modules.utils.files import *
from modules.utils.script_tools import boolean_emojis


energy_list = ['🌏 Сервер был перезапущен.\n\n⚡️ Энергия восполнена',
               '⚡️ Энергия восстановлена до максимума!',
               '⚡️ +1 к энергии']


def main():
    if config['password'] is None:
        client.start()
    else:
        client.start(password=config['password'])
    client.add_event_handler(user_handler)
    client.add_event_handler(game_handler)
    client.add_event_handler(peh_handler)
    asyncio.ensure_future(client.send_message('me', 'Бот запущен'))
    # asyncio.ensure_future(client.send_message(const['game'], '/hero'))
    read_file('hero')
    asyncio.ensure_future(status())
    client.run_until_disconnected()


async def status():
    HERO = hero['hero']
    GNR_CFG = hero['general_cfg']
    FARM_CFG = hero['farm_cfg']
    PROF_CFG = hero['prof_cfg']
    SPACE = hero['space']
    status_text = f"**Персонаж:** {HERO['name']}\n" \
                  f"**Лвл.:** {HERO['lvl']}\n" \
                  f"**Режим:** {hero['mode']}\n" \
                  f"**Последняя локация:** {hero['cur_loc']}\n" \
                  f"**Проход каптчи:** {boolean_emojis(GNR_CFG['captcha'])}\n" \
                  f"**Эдем:** {boolean_emojis(GNR_CFG['edem'])}\n" \
                  f"**Космос:** {boolean_emojis(SPACE['cosmos'])}\n\n" \
                  f"**===== ГРИНД =====**\n" \
                  f"**Лока:** {FARM_CFG['farm_loc']}\n" \
                  f"**Мобы:** {FARM_CFG['mob_lvl']} {FARM_CFG['mob_cls']}\n" \
                  f"**Гринд всех уровней:** {boolean_emojis(FARM_CFG['any_lvls'])}\n" \
                  f"**Обязательный хил:** {boolean_emojis(FARM_CFG['force_heal'])}\n\n" \
                  f"**===== ПРОФА =====**\n" \
                  f"**Ресурс:** {PROF_CFG['prof']}\n" \
                  f"**Лока:** {FARM_CFG['prof_loc']}\n" \
                  f"**Ловить редкие:** {boolean_emojis(PROF_CFG['catch_rare'])}\n" \
                  f"**Мультитул:** {boolean_emojis(PROF_CFG['multitool'])}\n\n" \
                  f"**===== КОСМОС =====**\n" \
                  f"**Ждать реса моба:** {boolean_emojis(not SPACE['cosmos_farm_seek'])}\n"
    await client.send_message('me', f"Загружены настройки: \n\n{status_text}")
    const['orig_msg_status'] = f'Включен режим **{hero["mode"]}**'
    const["msg_status"] = await client.send_message('me', const['orig_msg_status'])


if __name__ == '__main__':
    main()
