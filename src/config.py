import os

def style(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


URL = 'http://127.0.0.1:9097'
secret = None

LANG = 'en_us'

first_page = 'overview'
clash_path = 'clash'

with open('config.ini', 'r', encoding='utf-8') as file:
    for line in file:
        exec(line.strip())