from typing import Tuple
import numpy as np

def umbalanced(training:np.ndarray, testing:np.ndarray)->Tuple[np.ndarray, np.ndarray]:
    """Return data as-is, without any balancing approach."""
    return training, testing