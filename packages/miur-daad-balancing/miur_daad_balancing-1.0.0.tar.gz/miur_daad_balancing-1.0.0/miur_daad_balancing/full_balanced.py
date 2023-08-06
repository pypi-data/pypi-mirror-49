from typing import Tuple
from .utils import load_full_balanced
from .originals import sampling_class_portion
from .balanced import balanced
import numpy as np

def full_balanced(training:np.ndarray, testing:np.ndarray)->Tuple[np.ndarray, np.ndarray]:
    """Return full_balanced training data to the given maximum and testing data with updated proportions."""
    training, _ = balanced(training, testing)
    X_test, y_test = sampling_class_portion(testing[:-1], testing[-1], class_portion=load_full_balanced())
    return training, (*X_test, y_test)