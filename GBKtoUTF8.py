#!python3
import os

for path, dirs, files in os.walk('.'):
    for file in files:
        try:
            with open(os.path.join(path, file), 'r', encoding='gbk') as f:
                text = f.read()
            with open(os.path.join(path, file), 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            pass
