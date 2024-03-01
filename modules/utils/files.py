import json
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent


def read_file(file):
    file_name = ''
    if file == 'hero':
        file_name = f'{root_dir}\\configs\\my_hero.json'
    if file == 'config':
        file_name = f'{root_dir}\\configs\\tg_API.json'
    with open(file_name, encoding='utf-8') as json_file:
        loaded_json = json.load(json_file)
    return loaded_json


def update_file(dict_to_push):
    dict_cat = f"{dict_to_push=}".split("=")[0]
    file_name = ''
    if dict_cat == 'hero':
        file_name = f'{root_dir}\\configs\\my_hero.json'
    if dict_cat == 'config':
        file_name = f'{root_dir}\\configs\\tg_API.json'
    print(root_dir)
    # print(file_name)
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(dict_to_push, outfile, ensure_ascii=False, indent=2)
