#!python3
import os
import numpy as np
from PIL import Image


def jpeg2png(path, name, mask=(255, 255, 255), limit=32):
    img = Image.open(path)
    
    arr = np.array(img.convert('RGBA'))

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i,j,3] = 0x00 if np.all(np.abs(arr[i,j,:3] - mask) < limit) else 0xFF      # alhpa channel

    Image.fromarray(arr).save(f'{name}.png')


for name in os.listdir('.'):
    if name.endswith('.jpg') or name.endswith('.jpeg'):
        jpeg2png(os.path.join(os.getcwd(), name), name.split('.')[0])
