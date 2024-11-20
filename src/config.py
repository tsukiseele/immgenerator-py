# from collections import namedtuple

import json


class _SupportedFormats:
    min_inclusive: int
    max_inclusive: int
    def __init__(self, **entries):
        self.__dict__.update(entries)

class _Pack:
    pack_format: int
    description: str
    supported_formats: _SupportedFormats
    def __init__(self, **entries):
        self.__dict__.update(entries)
        obj = entries.get('supported_formats', None)
        if not obj == None:
            self.supported_formats = _SupportedFormats(**obj)

class _MCMeta: 
    pack: _Pack
    def __init__(self, **entries):
        self.__dict__.update(entries)
        obj = entries.get('pack', None)
        if not obj == None:
            self.pack = _Pack(**obj)
    
class Config:
    AUTHOR: str
    TITLE: str
    SIZE_4X: int
    SIZE_3X: int
    BLOCK_PIXEL_SIZE: int
    RESOLUTION: int
    IMAGE_FIT: bool
    IMAGE_MINILIZE: bool
    MCMETA: str
    # MCMETA: _MCMeta

    def __init__(self, **entries):
        self.__dict__.update(entries)
        # obj = entries.get('MCMETA', None)
        # if not obj == None:
        #     self.MCMETA = _MCMeta(**obj)
    # def toJson(self):
    #     json.dumps(self.__dict__) 