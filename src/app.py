import json
import os
import io
from .config import Config
from pathlib import Path
from types import SimpleNamespace

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = Path(dir_path).joinpath('config.json')

DEFAULT_CONFIG = """{
    "AUTHOR": "Nekoha Shizuku~",
    "TITLE": "しずくの日常🏠",
    "SIZE_4X": 2048,
    "SIZE_3X": 1024,
    "BLOCK_PIXEL_SIZE": 16,
    "RESOLUTION": 256,
    "IMAGE_FIT": true,
    "IMAGE_BORDER": {
        "enable": false,
        "borderSize": 10,
        "borderColor": {
            "r": 0,
            "g": 0,
            "b": 0,
            "alpha": 0
        }
    },
    "IMAGE_MINILIZE": false,
    "MCMETA": {
        "pack": {
            "pack_format": 16,
            "supported_formats": {
                "min_inclusive": 16,
                "max_inclusive": 1048576
            },
            "description": "Painting Pack made with IMMGenerator!"
        }
    }
}"""
CONFIG: Config = None

def get_config():
    global CONFIG
    return CONFIG

def initialize():
    isConfigExists = os.path.exists(config_path)
    if not isConfigExists:
        global CONFIG
        j = json.loads(DEFAULT_CONFIG) 
        CONFIG = Config(**j)
        f = open('config.json', 'w')
        f.write(json.dumps(CONFIG.__dict__))
        f.close()
    f = open('config.json', 'r')
    j = f.read()
    CONFIG = Config(**json.loads(j))
    f.close()

initialize()