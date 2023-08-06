import numpy as np
from typing import List, Dict

def sampling_class_portion(data:List[np.ndarray], classes:np.ndarray, class_portion:Dict):
    """
    Sampling data points in each class to keep a given portion among classes.
    class_portion: dict, the portion for each class, each value should be at least 1, e.g. class_portion={"class0":5,"class1":1,"class3":2}
    """
    u, indices = np.unique(classes, return_inverse=True)
    indices = np.asarray(indices)
    num_u = len(u)
    sample_sizes = dict()

    min_value = min([
        class_portion[c] for c in u
    ])
    class_portion = {
        k:v/min_value for k, v in class_portion.items()
    }

    # get sample size of each class
    size_min = float("inf")
    for i in range(num_u):
        sample_size_this = np.sum(indices == i)
        sample_sizes[u[i]] = sample_size_this        
        if class_portion[u[i]] == 1 and sample_size_this < size_min:
            size_min = sample_size_this

    indices_all = np.array([], dtype=indices.dtype)
    indices_range = np.array(range(len(indices)))

    # sampling
    for i in range(num_u):
        ind_this_num = indices_range[indices == i]
        replacetf = True if sample_sizes[u[i]] < (
            size_min*class_portion[u[i]]) else False
        ind_this_reduced = ind_this_num[np.random.choice(
            sample_sizes[u[i]], size=int(size_min*class_portion[u[i]]), replace=replacetf)]
        indices_all = np.append(indices_all, ind_this_reduced)

    # get the sampled data
    data = [
        d[indices_all, :] for d in data
    ]
    classes = classes[indices_all]
    return data, classes