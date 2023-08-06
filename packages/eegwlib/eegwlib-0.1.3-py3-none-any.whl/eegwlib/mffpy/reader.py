from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

import mffpy
from mffpy.epoch import Epoch
import numpy as np

from .bin_files import BinFile
from .segmentation import OutOfRangeError
from ..filter import filtfilt


class Reader(mffpy.Reader):  # type: ignore
    """Subclass of `segmentation.Reader` that adds segmentation capability"""

    @property
    def _eeg_bin(self) -> BinFile:
        """Return `BinFile` reader with EEG data"""
        for si in self.directory.signals_with_info():
            with self.directory.filepointer(si.info) as fp:
                info = mffpy.XML.from_file(fp)
            if info.generalInformation['channel_type'] == 'EEG':
                return BinFile(si.signal, info, 'EEG')
        raise FileNotFoundError('No EEG binary found')

    def enveloping_epoch(self, relative_time: float) -> Epoch:
        """Return the epoch which envelops `relative_time`

        Parameters
        ----------
        relative_time
            Time (seconds) relative to start of recording

        Returns
        -------
        The epoch which envelops `relative_time`

        Raises
        ------
        ValueError
            If `relative_time` does not fall within any epoch
        """
        for epoch in self.epochs:
            if epoch.t0 <= relative_time < epoch.t1:
                return epoch
        raise ValueError(f'Relative time [{relative_time}] '
                         'does not fall within any epochs')

    def extract_segments(self, relative_times: Dict[str, List[float]],
                         padl: float, padr: float, order: int = 4,
                         fmin: Optional[float] = None,
                         fmax: Optional[float] = None
                         ) -> Tuple[Dict[str, List[np.ndarray]],
                                    Dict[str, List[float]]]:
        """Extract segments around relative times

        Parameters
        ----------
        relative_times
            Dictionary of {category name: times (seconds)}. Times are relative
            to start of recording.
        padl
            Left time padding (seconds)
        padr
            Right time padding (seconds)
        order
            Filter order
        fmin
            Lower critical frequency (Hz) for IIR filter
        fmax
            Upper critical frequency (Hz) for IIR filter

        Returns
        -------
        segments
            Dictionary of {category name: segments} with the segments that
            were successfully extracted
        out_of_range_segs
            Dictionary of {category name: relative times} with relative times
            for which segments extended beyond the data range and could not
            be extracted

        Raises
        ------
        ValueError
            If `padl` or `padr` are negative
        """
        for var, value in {'left': padl, 'right': padr}.items():
            if value < 0:
                raise ValueError(f'Negative {var} padding: {value}')
        if fmin or fmax:
            # Extract filtered segments
            return self._extract_filtered_segments(relative_times, padl, padr, order, fmin, fmax)
        else:
            return self._extract_segments(relative_times, padl, padr)

    def _extract_segments(self, relative_times: Dict[str, List[float]],
                          padl: float, padr: float
                          ) -> Tuple[Dict[str, List[np.ndarray]],
                                     Dict[str, List[float]]]:
        """Extract unfiltered segments around relative times"""
        segments = defaultdict(list)
        out_of_range_segs = defaultdict(list)
        for cat, times in relative_times:
            for time in times:
                epoch = self.enveloping_epoch(time)
                time_relative_to_epoch = time - epoch.t0
                try:
                    segment = self._eeg_bin.extract_segment(
                        time_relative_to_epoch, padl, padr, epoch.block_slice
                    )
                    segments[cat].append(segment)
                except OutOfRangeError:
                    out_of_range_segs[cat].append(time)
        return segments, out_of_range_segs

    def _extract_filtered_segments(self,
                                   relative_times: Dict[str, List[float]],
                                   padl: float, padr: float, order: int,
                                   fmin: Optional[float],
                                   fmax: Optional[float]
                                   ) -> Tuple[Dict[str, List[np.ndarray]],
                                              Dict[str, List[float]]]:
        """Extract filtered segments around relative times"""
        segments = defaultdict(list)
        out_of_range_segs = defaultdict(list)
        for epoch in self.epochs:
            filtered_epoch = self.load_filtered_epoch(epoch, order, fmin, fmax)
            for cat, times in relative_times:
                for time in times:

    def load_filtered_epoch(self, epoch: Epoch, order: int,
                            fmin: Optional[float],
                            fmax: Optional[float]) -> np.ndarray:
        """Read and filter all EEG data in `epoch`"""
        eeg_data, _ = self.get_physical_samples_from_epoch(epoch,
                                                           channels=['EEG'])
        return filtfilt(eeg_data, self.sampling_rates['EEG'],
                        order, fmin, fmax)


    def _sort_relative_times_by_epoch(self,
                                      relative_times: Dict[str, List[float]]
                                      ) -> Dict[Any, dict]:
        """Sort relative times into dictionary of {epoch, {category, times}}"""
        times_by_epoch = defaultdict(dict)
        for cat, times in relative_times.items():
            for time in times:
                epoch = self.enveloping_epoch(time)
                if epoch not in times_by_epoch:
                    times_by_epoch[epoch] = defaultdict(list)
                times_by_epoch[epoch][cat].append(time)
        return times_by_epoch
