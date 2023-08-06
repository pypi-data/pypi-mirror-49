from typing import Callable
from .umbalanced import umbalanced
from .balanced import balanced
from .full_balanced import full_balanced

def get_callback(mode:str)->Callable:
    return {
        "umbalanced":umbalanced,
        "balanced":balanced,
        "full_balanced":full_balanced
    }[mode]