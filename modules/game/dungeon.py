import asyncio
from random import randint
from modules.starter.starter import client, hero, const


async def dungeon_handler(event):
    message = event.message
    text = message.message
    if '⚔️ Выберите действие:' in text or '⚔️ Цель для атаки:' in text or 'Выберите цель' in text:
        if 'Выберите цель' not in text:
            buttons = message['reply_markup']['rows']
            await asyncio.sleep(randint(1, 5))
            print(
                f'BUTTONS:\n{buttons[1]["buttons"][0]["text"]}\n{buttons[0]["buttons"][1]["text"]}\n{buttons[0]["buttons"][0]["text"]}')
            if '⏳' not in buttons[1]["buttons"][0]["text"]:
                await event.message.click(text=buttons[1]["buttons"][0]["text"])
            elif '⏳' not in buttons[0]["buttons"][1]["text"]:
                await event.message.click(text=buttons[0]["buttons"][1]["text"])
            elif '⏳' not in buttons[0]["buttons"][0]["text"]:
                await event.message.click(text=buttons[0]["buttons"][0]["text"])
            hero['target'] = 'none'
        elif 'Выберите цель' in text:
            targets_lines = text.split('\n')
            targets = []
            for t in targets_lines:
                if 'Выберите цель' not in t:
                    num = t.split(')')[0]
                    cur_hp = int(t.split('(💔')[1].split('/')[0])
                    max_hp = int(t.split('/')[1].split(')')[0])
                    link = t.split(') ')[2]
                    targets.append([num, cur_hp, max_hp, link])
            targets.sort(key=lambda x: x[1])
            print(targets)
            target = targets[-1]
            hero['target'] = target[3]
            await asyncio.sleep(randint(1, 3))
            await client.send_message(const["game"], hero['target'])
            await asyncio.sleep(randint(1, 2))
            await client.send_message(const["game"], target[0])
