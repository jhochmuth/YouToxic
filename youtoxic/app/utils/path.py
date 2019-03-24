import os
import youtoxic


def get_abs_path(relative_path):
    p = os.path.dirname(youtoxic.__file__)
    return os.path.join(p, relative_path)
