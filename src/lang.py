from src import config
import json

lang_file = f'./lang/{config.LANG}.json'
with open(lang_file, 'r', encoding='utf-8') as f:
    LANG:dict = json.load(f)


def get(id: str) -> str:
    """
    Get the language string for the given id.
    """
    return LANG.get(id, id)