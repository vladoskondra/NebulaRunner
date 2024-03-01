from modules.starter.starter import client, hero, const


async def do_heal():
    if hero['state'] == 'waiting for heal' and hero['mode'] != 'stop':
        await client.send_message(const["game"], '🛠 Техосмотр')
        const["last_action"] = '🛠 Техосмотр'
        hero['state'] = 'ready to leave Town'
