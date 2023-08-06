from typing import Dict
from .load_data import load_data

def load_full_balanced()->Dict:
    """Return the default parameters for the full_balanced setting."""
    return load_data("full_balanced")