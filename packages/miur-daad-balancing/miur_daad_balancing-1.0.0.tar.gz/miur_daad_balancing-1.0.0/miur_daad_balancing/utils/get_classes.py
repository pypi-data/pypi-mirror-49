from typing import List
from .load_full_balanced import load_full_balanced

def get_classes()->List[str]:
    """Return classes from full_balanced settings."""
    return list(load_full_balanced().keys())