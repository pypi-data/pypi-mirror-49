from typing import Tuple
from .utils import load_balanced
from .originals import truncate_sample_size
import numpy as np

def balanced(training:np.ndarray, testing:np.ndarray)->Tuple[np.ndarray, np.ndarray]:
    """Return balanced training data to the given maximum, leaving testing untouched."""
    X_train, y_train = truncate_sample_size(training[:-1], training[-1], max_size_given=load_balanced()["max"])
    return (*X_train, y_train), testing