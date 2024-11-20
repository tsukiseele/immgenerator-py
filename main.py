# import path from "node:path";
# import { createWriteStream } from "node:fs";
# // import fs from 'node:fs/promises'
# // import sizeOf from "image-size";
# import calcBlockSize from "./calc.ts";
# import { readPathInput, deepLoopTraversal } from "./utils.ts";
# import archiver from 'archiver'
# import { initialize } from "./app.ts";
# // import sharp from "sharp";
# import { Jimp } from "jimp";
# // import 
# // require("@img/sharp-win32-x64");
# // initialize
# await initialize()
from io import BytesIO
import json
import os
import time
from PIL import Image, ImageOps
from typing import List
from zipfile import ZipFile
from pathlib import Path
from src.app import get_config
from src.calc import calcBlockSize

CONFIG = get_config()

print('===================== CONFIG =====================');
print(json.dumps(CONFIG.__dict__))
print('==================================================');

cmd_input = input('Enter the image directory path(or drag the directory into the window):\r\n')

def deep_list_dir(dir: str, filter_suffix: List[str] = []) -> List[os.DirEntry[str]]: 
    entries = os.scandir(dir)
    results = []
    for entry in entries:
        if (entry.is_dir()):
            results.extend(deep_list_dir(entry, filter_suffix)) 
        else:
            _, file_extension = os.path.splitext(entry.path)
            if filter_suffix == None:
                results.append(entry)
            else:
                if file_extension in filter_suffix:
                    results.append(entry)
    return results

timestamp = time.time()
input_path = Path(cmd_input)
files = deep_list_dir(input_path, ['.png'])

output_path = input_path.parents[0].joinpath(f'{input_path.name}.zip')
package_name = f"nyarray_packs_{hash(time.time())}"
paintings = []
imageDataSet = []

for index, file in enumerate(files):
    image = Image.open(file)
    size = image.width, image.height
    blockSize = calcBlockSize(size[0], size[1]);
    x = blockSize[0]
    y = blockSize[1]

    if CONFIG.IMAGE_MINILIZE:
        size = image.width // 2, image.height // 2
        image.resize(size)
        
    if CONFIG.IMAGE_FIT:
        image = ImageOps.fit(image, [int(size[0] if x > y else size[1] * x / y), int(size[0] * y / x if x > y else size[1])], Image.Resampling.BICUBIC)

    imageDataSet.append(image)
    paintings.append({ 'name': str(index).zfill(3), 'w': x, 'h': y })

output_zip = ZipFile(output_path, 'w')
output_zip.writestr('pack.mcmeta', json.dumps(CONFIG.MCMETA))

for index, image in enumerate(imageDataSet):
    painting = paintings[index]
    image = imageDataSet[index]
    print(':', painting)
    paintingName = painting["name"]
    entryName = f'{CONFIG.TITLE} No. {paintingName}'
    entryPath = f'data/{package_name}/paintings/{paintingName}'
    wh = [painting['w'] // 16, painting['h'] // 16 ]
    
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    output_zip.writestr(f'{entryPath}.png', img_byte_arr)
    output_zip.writestr(f'{entryPath}.json', json.dumps({
        'name': entryName,
        'author': CONFIG.AUTHOR,
        'resolution': CONFIG.RESOLUTION,
        'width': wh[0],
        'height': wh[1]
    }))

output_zip.close()

input(f'{time.time() - timestamp}s')