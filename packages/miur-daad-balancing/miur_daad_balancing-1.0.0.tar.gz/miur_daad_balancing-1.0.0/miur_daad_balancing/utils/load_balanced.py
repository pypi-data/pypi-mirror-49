from typing import Dict
from .load_data import load_data

def load_balanced()->Dict:
    """Return the default parameters for the balanced setting."""
    return load_data("balanced")