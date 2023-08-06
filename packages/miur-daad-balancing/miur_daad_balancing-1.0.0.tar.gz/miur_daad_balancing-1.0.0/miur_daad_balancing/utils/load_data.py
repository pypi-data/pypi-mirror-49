from typing import Dict
from .current_path import current_path
from json import load

def load_data(file_path: str)->Dict:
    with open("{p}/{f}.json".format(p=current_path(), f=file_path), "r") as f:
        return load(f)
