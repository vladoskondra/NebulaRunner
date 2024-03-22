import json
import os
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent


def read_file(file):
    file_name = ''
    raw = {}
    if file == 'hero':
        file_name = f'{root_dir}/configs/my_hero.json'
        with open(f'{root_dir}/configs/template_hero.json', encoding='utf-8') as json_file:
            raw = json.load(json_file)
    if file == 'config':
        file_name = f'{root_dir}/configs/tg_API.json'
        raw = {
            "api_id": 0,
            "api_hash": "",
            "password": "-"
        }
    # print(f"is_dir? {Path(f'{root_dir}/configs').is_dir()}")
    # print(f"is_file? {Path(file_name).is_file()}")
    if Path(f'{root_dir}/configs').is_dir() and Path(file_name).is_file():
        check_file_structure(file)
        with open(file_name, encoding='utf-8') as json_file:
            loaded_json = json.load(json_file)
    else:
        loaded_json = raw
        update_file(file, raw)
    return loaded_json


def update_file(category, data):
    file_name = ''
    if category == 'hero':
        file_name = f'{root_dir}/configs/my_hero.json'
    if category == 'config':
        file_name = f'{root_dir}/configs/tg_API.json'
    if not Path(f'{root_dir}/configs').is_dir():
        os.makedirs(f'{root_dir}/configs')
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)


def check_file_structure(file):
    if file == 'hero':
        with open(f'{root_dir}/configs/template_hero.json', encoding='utf-8') as temp_file:
            temp = json.load(temp_file)
        with open(f'{root_dir}/configs/my_hero.json', encoding='utf-8') as my_file:
            check_file = json.load(my_file)
        for t in temp:
            if t not in check_file:
                check_file[t] = temp[t]
            if type(temp[t]) == dict:
                sub = temp[t]
                for s in sub:
                    if s not in check_file[t]:
                        check_file[t][s] = sub[s]
    elif file == 'config':
        with open(f'{root_dir}/configs/template_API.json', encoding='utf-8') as temp_file:
            temp = json.load(temp_file)
        with open(f'{root_dir}/configs/tg_API.json', encoding='utf-8') as my_file:
            check_file = json.load(my_file)
        for t in temp:
            if t not in check_file:
                check_file[t] = temp[t]
            if type(temp[t]) == dict:
                sub = temp[t]
                for s in sub:
                    if s not in check_file[t]:
                        check_file[t][s] = sub[s]
    print(f"UPDATING STRUCTURE OF CONFIG FILE: {file}")
    update_file(file, check_file)
#
#
# if __name__ == '__main__':
#     check_file_structure('hero')