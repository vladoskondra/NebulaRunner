import random
from modules.starter.starter import client, const


def flatten_extend(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list


def boolean_emojis(bool_emoji):
    emoji = '✅' if bool_emoji else '❌'
    return emoji


def gen_rnd():
    rnd_num = random.randint(0, 10000)
    return rnd_num


async def change_status(text):
    new_status = f"{const['orig_msg_status']}\n\n[{gen_rnd()}] Статус: {text}"
    try:
        await client.edit_message('me', const["msg_status"], new_status)
    except:
        print(f"Can't change status message to: {text}")
