# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Functions that are needed throughout the project
# ----------------------------

import time
from .const import session_statuses


# TODO: consider making a more complex timing decorator (log to file, upload to db, ...)
def timeit(method):
    """
    Decorator function that prints the time required for the provided method to compute

    :param method: The method to be timed
    :return: The function corresponding to the decorator, in order to make it callable
    """

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' %\
              (method.__name__, (te - ts) * 1000))
        return result

    return timed
