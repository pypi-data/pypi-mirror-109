import numpy as np


def seconds_to_samples(seconds: float, sr: float) -> int:
    """Convert seconds to samples, rounding to the nearest sample"""
    return int(np.round(seconds * sr))


def extract_segment_from_array(arr: np.ndarray, center: float, padl: float,
                               padr: float, sr: float) -> np.ndarray:
    """Extract a segment from array of signal data

    Parameters
    ----------
    arr
        Array from which to extract segment
    center
        The center of the segment in seconds relative to the beginning of `arr`
    padl
        Left time padding (seconds)
    padr
        Right time padding (seconds)
    sr
        Sampling rate of the signal data

    Returns
    -------
    The extracted segment

    Raises
    ------
    ValueError
        If the loaded data block is not a 2-dimensional array
    OutOfRangeError
        If the requested segment extends beyond the data block
    """
    if len(arr.shape) != 2:
        raise ValueError('Input array must be 2-dimensional. '
                         f'Got shape: {arr.shape}')
    # Start index of right side of segment
    right_start_idx = seconds_to_samples(center, sr)
    left_samples = seconds_to_samples(padl, sr)
    right_samples = seconds_to_samples(padr, sr)
    # Start index of whole segment
    segment_start_idx = right_start_idx - left_samples
    # Stop index of whole segment
    segment_stop_idx = right_start_idx + right_samples
    if segment_start_idx < 0:
        raise OutOfRangeError('Requested segment extends '
                              'beyond data block')
    if segment_stop_idx > arr.shape[1]:
        raise OutOfRangeError('Requested segment extends '
                              'beyond data block')
    segment_indices = np.array(range(segment_start_idx, segment_stop_idx))
    return arr.take(segment_indices, axis=1)


class OutOfRangeError(Exception):
    """Raised when a requested block slice extends beyond data range"""
    pass
