from modules.starter.starter import config
from modules.me_handler import *
from modules.game_handler import *
from modules.peh.peh import peh_handler
from modules.utils.files import *


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
    status_text = ''
    for i in hero:
        status_text += f"{i}: {hero[i]}\n"
    await client.send_message('me', f"Загружены настройки: \n\n{status_text}")
    const['orig_msg_status'] = f'Включен режим **{hero["mode"]}**'
    const["msg_status"] = await client.send_message('me', const['orig_msg_status'])


if __name__ == '__main__':
    main()
