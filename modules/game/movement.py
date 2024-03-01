from modules.starter.starter import client, hero, const


async def do_move():
    if (hero['loc'] == 'Town' or hero['loc'] == 'default') and (hero['mode'] == 'farm' or hero['mode'] == 'boost'):
        hero['state'] = 'ready to leave Town'
        await client.send_message(const["game"], '🗺 Локации')
        const["last_action"] = '🗺 Локации'
