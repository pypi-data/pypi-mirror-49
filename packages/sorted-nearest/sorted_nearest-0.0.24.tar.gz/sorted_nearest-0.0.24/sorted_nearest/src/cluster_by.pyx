

from libc.stdint cimport int32_t

cimport cython

import numpy as np

def annotate_clusters(starts, ends, ids, slack):

    if starts.dtype == np.long:
        return annotate_clusters64(starts, ends, ids, slack)
    elif starts.dtype == np.int32:
        return annotate_clusters32(starts, ends, ids, slack)
    else:
        raise Exception("Starts/Ends not int64 or int32: " + str(starts.dtype))


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cpdef annotate_clusters64(const long [::1] starts, const long [::1] ends, const long [::1] ids, int slack):

    cpdef int min_start = starts[0]
    cpdef int max_end = ends[0]
    cpdef int i = 0
    cpdef int n_clusters = 0
    cpdef int length = len(starts)

    output_arr_ids = np.ones(length, dtype=np.long) * -1

    cdef int32_t [::1] output_ids

    output_ids = output_arr_ids

    for i in range(length):
        if not (starts[i] - slack) <= max_end:
            output_ids[n_clusters] = ids[i]
            min_start = starts[i]
            max_end = ends[i]
            n_clusters += 1
        else:
            output_ids[n_clusters] = ids[i]
            if ends[i] > max_end:
                max_end = ends[i]

    if n_clusters != length:
        output_arr_ids[n_clusters] = ids[i]
        n_clusters += 1

    return output_arr_ids[:n_clusters]


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cpdef annotate_clusters32(const int32_t [::1] starts, const int32_t [::1] ends, const int32_t [::1] ids, int slack):

    cpdef int min_start = starts[0]
    cpdef int max_end = ends[0]
    cpdef int i = 0
    cpdef int n_clusters = 0
    cpdef int length = len(starts)

    output_arr_ids = np.ones(length, dtype=np.int32) * -1

    cdef int32_t [::1] output_ids

    output_ids = output_arr_ids

    for i in range(length):
        if not (starts[i] - slack) <= max_end:
            output_ids[n_clusters] = ids[i]
            min_start = starts[i]
            max_end = ends[i]
            n_clusters += 1
        else:
            output_ids[n_clusters] = ids[i]
            if ends[i] > max_end:
                max_end = ends[i]

    if n_clusters != length:
        output_arr_ids[n_clusters] = ids[i]
        n_clusters += 1

    return output_arr_ids[:n_clusters]
