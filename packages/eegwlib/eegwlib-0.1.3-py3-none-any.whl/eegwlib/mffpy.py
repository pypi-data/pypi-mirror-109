from typing import List, Optional, Tuple

import numpy as np
import mffpy
from mffpy.epoch import Epoch

from .filter import filtfilt


class ReaderMixIn:
    def _seconds_to_samples(self, seconds: float) -> int:
        """Convert seconds to samples, rounding to nearest sample"""
        return int(np.round(seconds * self.sampling_rates['EEG']))

    def _get_filtered_eeg_from_epoch(self, epoch: Epoch, t0: float,
                                     dt: float, extra_padding: float,
                                     order: int = 4,
                                     fmin: Optional[float] = None,
                                     fmax: Optional[float] = None
                                     ) -> np.ndarray:
        """Return filtered EEG signal data from epoch

        Parameters
        ----------
        epoch
            The epoch from which to extract EEG data
        t0
            Start time of EEG block to extract in seconds relative to start
            of epoch
        dt
            Duration of EEG block to extract (sec)
        extra_padding
            Time padding (sec) be applied to either side of the EEG block to
            minimize edge effects of filtering. The extra-padded EEG block is
            extracted, filtered, and then the extra padding is cropped out.
        order
            Filter order for filter to be applied
        fmin
            Lower critical frequency (Hz) for filter to be applied
        fmax
            Upper critical frequency (Hz) for filter to be applied

        Returns
        -------
        data_cropped
            The filtered EEG data

        Raises
        ------
        ValueError
            If `t0`, `dt`, or `extra_padding` are negative
        OutOfRangeError
            If the requested time slice is not contained with `epoch`
        """
        for var, value in {'t0': t0, 'dt': dt,
                           'extra_padding': extra_padding}.items():
            if value < 0:
                raise ValueError(f'Negative {var}: {value}')
        t0 = t0 - extra_padding
        if t0 < 0:
            raise OutOfRangeError('Requested block extends before epoch start')
        dt = dt + extra_padding * 2
        if t0 + dt > epoch.dt:
            raise OutOfRangeError('Requested block extends beyond epoch end')
        data = self.get_physical_samples_from_epoch(epoch, t0=t0, dt=dt,
                                                    channels=['EEG'])['EEG'][0]
        data_filtered = filtfilt(data, sr=self.sampling_rates['EEG'],
                                 order=order, fmin=fmin, fmax=fmax)
        # Crop the filtered data array
        extra_samples = self._seconds_to_samples(extra_padding)
        indices = np.array(
            range(extra_samples, data_filtered.shape[1] - extra_samples)
        )
        data_cropped = data_filtered.take(indices, axis=1)
        return data_cropped

    def get_filtered_eeg_from_epoch(self, epoch: Epoch, t0: float, dt: float,
                                    extra_padding: float, order: int = 4,
                                    fmin: Optional[float] = None,
                                    fmax: Optional[float] = None
                                    ) -> np.ndarray:
        """Return filtered EEG signal data from epoch

        Parameters
        ----------
        epoch
            The epoch from which to extract EEG data
        t0
            Start time of EEG block to extract in seconds relative to start
            of epoch
        dt
            Duration of EEG block to extract (sec)
        extra_padding
            Time padding (sec) be applied to either side of the EEG block to
            minimize edge effects of filtering. The extra-padded EEG block is
            extracted, filtered, and then the extra padding is cropped out.
        order
            Filter order for filter to be applied
        fmin
            Lower critical frequency (Hz) for filter to be applied
        fmax
            Upper critical frequency (Hz) for filter to be applied

        Returns
        -------
        data
            The filtered EEG data

        Notes
        -----
        To ensure this function always returns an array of the same length for
        a given `dt` value, `t0`, `dt` and `extra_padding` are rounded to the
        nearest sample.
        """
        # Round `t0`, `dt` and `extra_padding` to the nearest sample
        sr = self.sampling_rates['EEG']
        t0 = self._seconds_to_samples(t0) / sr
        dt_samples = self._seconds_to_samples(dt)
        dt = dt_samples / sr
        extra_padding = self._seconds_to_samples(extra_padding) / sr
        data = self._get_filtered_eeg_from_epoch(
            epoch, t0=t0, dt=dt, extra_padding=extra_padding,
            order=order, fmin=fmin, fmax=fmax
        )
        assert data.shape[1] == dt_samples
        return data

    def extract_segments(self, relative_times: List[float], padl: float,
                         padr: float, extra_padding: float,
                         order: int = 4, fmin: Optional[float] = None,
                         fmax: Optional[float] = None
                         ) -> Tuple[List[np.ndarray], List[float]]:
        """Extract filtered segments around relative times

        Parameters
        ----------
        relative_times
            List of times in seconds relative to startdatetime around which
            to create segments
        padl
            Left time padding (sec)
        padr
            Right time padding (sec)
        extra_padding
            Time padding (sec) be applied to either side of each segment to
            minimize edge effects of filtering. The extra-padded segment is
            extracted, filtered, and then the extra padding is cropped out.
        order
            Filter order for filter to be applied
        fmin
            Lower critical frequency (Hz) for filter to be applied
        fmax
            Upper critical frequency (Hz) for filter to be applied

        Returns
        -------
        segments
            List of the data segments that were successfully extracted
        out_of_range_segs
            List of the relative times for which segments extended beyond the
            data range and could not be extracted

        Raises
        ------
        ValueError
            If `padl` or `padr` are negative
        ValueError
            If `relative_times` contains any times that are not present in any
            epochs
        """
        for var, value in {'left padding': padl,
                           'right padding': padr}.items():
            if value < 0:
                raise ValueError(f'Negative {var}: {value}')
        segments = []
        out_of_range_segs = []
        dt = padl + padr
        for center in relative_times:
            epoch_with_center = None
            for epoch in self.epochs:
                if epoch.t0 < center < epoch.t1:
                    epoch_with_center = epoch
            if not epoch_with_center:
                raise ValueError(f'Relative time [{center}] not '
                                 'present in any epochs')
            t0 = center - padl - epoch_with_center.t0
            try:
                segment = self.get_filtered_eeg_from_epoch(
                    epoch_with_center, t0=t0, dt=dt,
                    extra_padding=extra_padding, order=order,
                    fmin=fmin, fmax=fmax
                )
                segments.append(segment)
            except OutOfRangeError:
                out_of_range_segs.append(center)
        # Sanity check
        assert len(segments) + len(out_of_range_segs) == len(relative_times)
        return segments, out_of_range_segs


class Reader(ReaderMixIn, mffpy.Reader):  # type: ignore
    def __init__(self, filename: str) -> None:
        super().__init__(filename)


class OutOfRangeError(Exception):
    """Raised when a requested block slice extends beyond data range"""
    pass
