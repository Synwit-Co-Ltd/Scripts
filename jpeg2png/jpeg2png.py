#!python3
import os
import numpy as np
from PIL import Image


def jpeg2png(path, name, mask=(255, 255, 255), limit=32):
    img = Image.open(path)
    
    arr = np.array(img.convert('RGBA'))

    arr[:,:,3] = np.where(np.all(np.abs(arr[:,:,:3] - mask) < limit, axis=2), 0x00, 0xFF)   # alpha channel

    Image.fromarray(arr).save(f'{name}.png')


for name in os.listdir('.'):
    if name.endswith('.jpg') or name.endswith('.jpeg'):
        jpeg2png(os.path.join(os.getcwd(), name), name.split('.')[0])
