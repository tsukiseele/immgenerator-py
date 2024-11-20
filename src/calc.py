
from .app import get_config

CONFIG = get_config()
def calcAbsRatio(width: int, height: int) -> float:
    whRatio = height / width if width > height else width / height
    if (whRatio > 0.75):
        return 0.75
    if (whRatio > 2 / 3):
        return 2 / 3
    if (whRatio > 0.5):
        return 0.5
    return 1

def calcMaxBlockSize(width: int, height: int, absRatio: float):
    maxPixelSize = width if width > height else height
    blockSize = 1
    if (maxPixelSize > CONFIG.SIZE_4X):
        blockSize = 4
    elif (maxPixelSize > CONFIG.SIZE_3X):
        blockSize = 3
    else:
        blockSize = 2
    
    maxSize = blockSize * CONFIG.BLOCK_PIXEL_SIZE
    minSize = maxSize * absRatio
    offset = minSize % CONFIG.BLOCK_PIXEL_SIZE
    if (offset != 0):
        if (offset > CONFIG.BLOCK_PIXEL_SIZE / 2):
            minSize = minSize - offset + CONFIG.BLOCK_PIXEL_SIZE
        else:
            minSize = minSize - offset;
    if (width > height):
        return [ int(maxSize), int(minSize) ]
    else:
        return [ int(minSize), int(maxSize) ]

def calcBlockSize(width: int, height: int):
    ratio = calcAbsRatio(width, height)
    return calcMaxBlockSize(width, height, ratio)
