import numpy as np


def seconds_to_samples(seconds: float, sr: float) -> int:
    """Convert seconds to samples, rounding to the nearest sample"""
    return int(np.round(seconds * sr))


def crop(array: np.ndarray, nsamples: int) -> np.ndarray:
    """Remove `nsamples` from both sides of `array` along the last axis"""
    data_slice = slice(nsamples, array.shape[-1] - nsamples)
    return array[..., data_slice]


class OutOfRangeError(Exception):
    """Raised when a requested block slice extends beyond data range"""
    pass
