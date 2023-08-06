from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import mffpy
from mffpy.epoch import Epoch
import numpy as np

from .bin_files import BinFile
from .utils import extract_segment_from_array, OutOfRangeError
from ..filter import filtfilt


class Segmenter(mffpy.Reader):
    """Subclass of `segmentation.Reader` that adds functionality to extract
    segments"""

    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._data_cache = None

    @property
    def data_cache(self):
        """Return value in data cache"""
        return self._data_cache

    def get_loaded_data(self) -> np.ndarray:
        """Retrieve loaded data block from data cache

        Raises
        ------
        AssertionError
            If no data is loaded
        """
        assert self.data_cache is not None, 'No data loaded'
        return self.data_cache

    def load_filtered_epoch(self, epoch: Epoch, order: int,
                            fmin: Optional[float],
                            fmax: Optional[float]) -> None:
        """Read and filter all EEG data in `epoch`, load into data cache

        Raises
        ------
        AssertionError
            If a data block is already loaded into data cache
        """
        assert self.data_cache is None, 'A data block is already loaded. ' \
                                        'First, clear loaded data.'
        data = self.get_physical_samples_from_epoch(epoch, channels=['EEG'])
        eeg_data = data['EEG'][0]
        self._data_cache = filtfilt(eeg_data, self.sampling_rates['EEG'],
                                    order, fmin, fmax)

    def clear_loaded_data(self) -> None:
        """Clear data from data cache"""
        self._data_cache = None

    @property
    def _eeg_bin(self) -> BinFile:
        """Return `BinFile` reader with EEG data"""
        for si in self.directory.signals_with_info():
            with self.directory.filepointer(si.info) as fp:
                info = mffpy.XML.from_file(fp)
            if info.generalInformation['channel_type'] == 'EEG':
                return BinFile(si.signal, info, 'EEG')
        raise FileNotFoundError('No EEG binary found')

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
            # Apply filter before extracting segments
            return self._extract_filtered_segments(relative_times, padl, padr,
                                                   order, fmin, fmax)
        else:
            # Extract unfiltered segments
            return self._extract_segments(relative_times, padl, padr)

    def _extract_segments(self, relative_times: Dict[str, List[float]],
                          padl: float, padr: float
                          ) -> Tuple[Dict[str, List[np.ndarray]],
                                     Dict[str, List[float]]]:
        """Extract unfiltered segments around relative times"""
        segments = defaultdict(list)
        out_of_range_segs = defaultdict(list)
        for cat, times in relative_times.items():
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
            self.clear_loaded_data()
            for cat, times in relative_times.items():
                for time in times:
                    if self.is_in_epoch(time, epoch):
                        time_relative_to_epoch = time - epoch.t0
                        if self.data_cache is None:
                            self.load_filtered_epoch(epoch, order, fmin, fmax)
                        try:
                            segment = self.extract_segment_from_loaded_data(
                                time_relative_to_epoch, padl, padr)
                            segments[cat].append(segment)
                        except OutOfRangeError:
                            out_of_range_segs[cat].append(time)
        self.clear_loaded_data()
        return segments, out_of_range_segs

    def is_in_epoch(self, relative_time: float, epoch: Epoch) -> bool:
        """Return `True` if `epoch` contains `relative_time`"""
        if epoch.t0 <= relative_time < epoch.t1:
            return True
        else:
            return False

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
            if self.is_in_epoch(relative_time, epoch):
                return epoch
        raise ValueError(f'Relative time [{relative_time}] '
                         'does not fall within any epochs')

    def extract_segment_from_loaded_data(self, center: float, padl: float,
                                         padr: float) -> np.ndarray:
        """Extract a segment from data block in data cache`

        Parameters
        ----------
        center
            The center of the segment in seconds relative to the beginning
            of the data block from which to extract
        padl
            Left time padding (seconds)
        padr
            Right time padding (seconds)

        Returns
        -------
        The extracted segment
        """
        return extract_segment_from_array(self.get_loaded_data(), center, padl,
                                          padr, self.sampling_rates['EEG'])
