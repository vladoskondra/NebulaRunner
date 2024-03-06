import json
import os
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent


def read_file(file):
    file_name = ''
    raw = {}
    if file == 'hero':
        file_name = f'{root_dir}/configs/my_hero.json'
        raw = {
            "name": "",
            "cur_hp": 0,
            "max_hp": 0,
            "lvl": 0,
            "energy": 5,
            "state": "none",
            "captcha": False,
            "mode": "stop",
            "intox": False,
            "target": "",
            "mob_lvl": 1,
            "mob_cls": "any",
            "farm_loc": "",
            "loc": "default",
            "prof": "none",
            "prof_loc": "",
            "edem": False,
            "multitool": False,
            "cosmos": False,
            "stats": {
                "class": "none",
                "atk": 1,
                "def": 1,
                "ddg": 0,
                "crit": 0,
                "acc": 0,
                "spd": 0
            }
        }
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
