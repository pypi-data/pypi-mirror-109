import mffpy.bin_files
import numpy as np

from .utils import seconds_to_samples, OutOfRangeError


class BinFile(mffpy.bin_files.BinFile):  # type: ignore
    """Subclass of `segmentation.bin_files.BinFile` that adds ability to extract
    data segments"""

    def extract_segment(self, center: float, padl: float, padr: float,
                        block_slice: slice) -> np.ndarray:
        """Extract a data segment from `block_slice`

        Parameters
        ----------
        center
            Center of the requested segment in seconds relative to the
            beginning of `block_slice`
        padl
            Left side of the requested segment (seconds)
        padr
            Right side of the requested segment (seconds)
        block_slice
            Data blocks from which the segment will be extracted. This is
            typically the block slice of the epoch containing the requested
            segment.

        Returns
        -------
        data
            Array of (channels, samples) containing the data segment
        """
        sr = self.signal_blocks['sampling_rate']
        # Start index of right side of segment
        right_start_idx = seconds_to_samples(center, sr)
        left_samples = seconds_to_samples(padl, sr)
        right_samples = seconds_to_samples(padr, sr)
        # Start index of whole segment
        segment_start_idx = right_start_idx - left_samples
        # Stop index of whole segment
        segment_stop_idx = right_start_idx + right_samples
        raw_samples = self.read_raw_samples_from_indices(segment_start_idx,
                                                         segment_stop_idx,
                                                         block_slice)
        data = (self.calibration * self.scale * raw_samples).astype(np.float32)
        #print(f'Data length: {data_cropped.shape[1]}')
        #print(f'Left samples: {left_samples}')
        #print(f'Right samples: {right_samples}')
        assert data.shape[1] == left_samples + right_samples
        return data

    def read_raw_samples_from_indices(self, a: int, b: int,
                                      block_slice: slice) -> np.ndarray:
        """Return array of raw samples that fall between indices `a` and `b`

        The signal data are organized in variable-sized blocks that enclose
        epochs of continuous recordings.  Discontinuous breaks can happen in
        between blocks.  `block_slice` indexes into such epochs, but we might
        want only a small chunk of it given by `a` and `b`. Therefore, we
        further index into blocks `bsi` selected through `block_slice` with the
        variables `A` and `B`.  Block indices `A` and `B` are chosen to enclose
        the interval `(a, b)` which we would like to read.

        This method is very similar to `read_raw_samples` except that it starts
        from sample indices instead of relative times.

        Parameters
        ----------
        a
            Index of the first sample to be read, relative to the beginning of
            `block_slice`
        b
            Index at which to stop reading data, relative to the beginning of
            `block_slice`
        block_slice
            Blocks to consider when reading data

        Returns
        -------
        block_data
            Array of shape (channels, samples) containing all data in range
            `(a, b)`

        Raises
        ------
        ValueError
            If `a` is greater than or equal to `b`
        OutOfRangeError
            If the requested data range extends beyond `block_slice`
        """
        if a >= b:
            raise ValueError(f'Start index ({a}) >= stop index ({b})')
        if a < 0:
            raise OutOfRangeError('Requested data extends beyond block slice')
        samples_in_block_slice = self.block_start_idx[block_slice.stop] - \
            self.block_start_idx[block_slice.start]
        #print(f'b: {b}')
        #print(f'Samples in block slice: {samples_in_block_slice}')
        if b > samples_in_block_slice:
            raise OutOfRangeError('Requested data extends beyond block slice')
        # Calculate the (relative) block index enclosing
        # `bsi[0]+a` and `bsi[0]+b`
        bsi = self.block_start_idx[block_slice]
        A = bsi.searchsorted(bsi[0] + a, side='right') - 1
        B = bsi.searchsorted(bsi[0] + b, side='left')
        # Calculate the relative sample size index with respect to
        # the blocks that indices (A, B) determine.
        a -= bsi[A] - bsi[0]
        b -= bsi[A] - bsi[0]
        # Calculate the (absolute) block index enclosing <..>
        A += block_slice.start
        B += block_slice.start
        # Read the enclosing blocks
        block_data = self._read_blocks(A, B)
        # Reject offsets (a, b) that go beyond requested range
        block_data = block_data[:, a:b]
        return block_data
