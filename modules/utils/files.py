import json
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent


def read_file(file):
    file_name = ''
    if file == 'hero':
        file_name = './../../../configs/my_hero.json'
    if file == 'config':
        file_name = './../../../configs/tg_API.json'
    with open(file_name, encoding='utf-8') as json_file:
        loaded_json = json.load(json_file)
    return loaded_json


def update_file(category, data):
    file_name = ''
    if category == 'hero':
        file_name = './../../../configs/my_hero.json'
    if category == 'config':
        file_name = './../../../configs/tg_API.json'
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
