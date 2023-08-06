import numpy as np
from typing import List

def truncate_sample_size(data:List[np.ndarray], classes, others=None, max_size_given=None):
    """
    Balance sample size of a data set among classes.

    INPUTS:
    data: numpy 2d array or matrix, each row should be a sample.

    classes: numpy 1d array or vector, class labels.

    others: numpy 2d array or matrix, extra information of samples if available,
    each row should associated to a row of data.

    min_size_given: int, the size of each class wanted.

    rng: numpy random state.

    OUTPUTS:
    data: numpy 2d array or matrix, each row should be a sample, balanced data.

    classes: numpy 1d array or vector, balanced class labels.

    indices_all: numpy 1d array, the numerical indices of samples selected.
    others: numpy 2d array or matrix, balanced other information.

    Example:
    data=[[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6],[7,7,7]]
    data=np.array(data)
    classes=np.array(['zz','xx','xx','yy','zz','yy','xx'])
    balance_sample_size(data,classes,others=NOne,max_size_given=50)
    """
    u, indices = np.unique(classes, return_inverse=True)
    indices = np.asarray(indices)
    num_u = len(u)
    sample_sizes = []

    # get sample size of each class
    for i in range(num_u):
        sample_size_this = np.sum(indices == i)
        sample_sizes.append(sample_size_this)
    sample_sizes = np.array(sample_sizes, dtype=int)

    size_max = np.amax(sample_sizes)  # largest sample size

    if size_max < max_size_given:
        max_size_given = size_max
    sample_sizes[sample_sizes > max_size_given] = max_size_given

    indices_all = np.array([], dtype=indices.dtype)
    indices_range = np.array(range(len(indices)))

    for i in range(num_u):
        ind_this_num = indices_range[indices == i]
        ind_this_reduced = ind_this_num[np.random.choice(
            len(ind_this_num), size=sample_sizes[i], replace=False)]
        indices_all = np.append(indices_all, ind_this_reduced)

    # reduce the data
    data = [
        d[indices_all, :] for d in data
    ]
    classes = classes[indices_all]
    if np.any(others):
        others = others[indices_all]
    return data, classes