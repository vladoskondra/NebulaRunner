import asyncio
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
from telethon.tl.types import MessageEntityTextUrl
from modules.starter.starter import client, hero
from modules.utils.get_chrome_version import get_chrome_version


async def solve_captcha(event):
    if hero['captcha']:
        try:
            message = event.message
            print('КАПТЧА')
            print(event)
            url = ''
            if 'reply_markup' in message:
                print('true reply')
                reply_markup = message['reply_markup']
                url = reply_markup['rows'][0]['buttons'][0]['url']
                print(url)
            else:
                entities = event.message.entities
                for ent in entities:
                    if isinstance(ent, MessageEntityTextUrl):
                        if "llab.orion-nebula.space" in ent.url:
                            url = ent.url
            await asyncio.sleep(randint(5, 9))
            dr = uc.Chrome(service=ChromeService(ChromeDriverManager(driver_version=get_chrome_version()).install()))
            dr.get(url)
            await asyncio.sleep(randint(3, 6))
            await asyncio.sleep(20)
        except:
            await client.send_message('me', 'Не удалось пройти капчу, нужно смотреть ошибку.\nБот выключен')
            hero['mode'] = 'stop'
    else:
        await client.send_message('me', 'КАПЧА, бот выключен.\n'
                                        'После прохождения капчи, пропиши нужный режим, чтоб продолжить работу бота')
        hero['mode'] = 'stop'
