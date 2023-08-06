import numpy as np
from enum import Enum
from functools import partial


def approximate_reconstruction(rp_x, rp_anchor, rp_anchored):
    rp_approximate = rp_anchored - rp_anchor - rp_x
    return rp_approximate.astype(np.float32)


def full_reconstruction(rp_x, rp_anchor, rp_anchored):
    rp_approximate = approximate_reconstruction(rp_x, rp_anchor, rp_anchored)

    rp_anchor[rp_anchor == 0] = 1
    # rp_approximate is float32, np.sqrt of a uint8 returns a float16, division returns a float23
    return rp_approximate / (- 2 * np.sqrt(rp_anchor))


def sign_reconstruction(rp_x, rp_anchor, rp_anchored):
    rp_approximate = approximate_reconstruction(rp_x, rp_anchor, rp_anchored)
    # rp_approximate is float32, sign is float32, multiplication returns a float32
    return np.sign(rp_approximate) * np.sqrt(rp_x)


class ReconstructionStrategy(Enum):
    """Enum for selecting strategy of pseudo-linear reconstruction"""
    FULL = partial(full_reconstruction)
    SIGN = partial(sign_reconstruction)
    APPROXIMATE = partial(approximate_reconstruction)

    def __call__(self, *args):
        return self.value(*args)
