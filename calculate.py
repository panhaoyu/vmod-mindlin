import math
import numpy as np


def get_Fii(a: np.float_, b: np.float_):
    divide = a / b
    divide_reverse = 1 / divide
    temp = np.sqrt(divide ** 2 + 1)
    return 2 * divide * (np.log(1 / divide))
