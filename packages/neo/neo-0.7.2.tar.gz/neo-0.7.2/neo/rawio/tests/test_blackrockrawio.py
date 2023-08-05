# -*- coding: utf-8 -*-
"""
Tests of neo.rawio.examplerawio
"""

# needed for python 3 compatibility
from __future__ import unicode_literals, print_function, division, absolute_import

import unittest

from neo.rawio.blackrockrawio import BlackrockRawIO
from neo.rawio.tests.common_rawio_test import BaseTestRawIO

import numpy as np
from numpy.testing import assert_equal

try:
    import scipy.io

    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


class TestBlackrockRawIO(BaseTestRawIO, unittest.TestCase, ):
    rawioclass = BlackrockRawIO
    entities_to_test = ['FileSpec2.3001']

    files_to_download = [
        'FileSpec2.3001.nev',
        'FileSpec2.3001.ns5',
        'FileSpec2.3001.ccf',
        'FileSpec2.3001.mat',
        'blackrock_2_1/l101210-001.mat',
        'blackrock_2_1/l101210-001_nev-02_ns5.mat',
        'blackrock_2_1/l101210-001.ns2',
        'blackrock_2_1/l101210-001.ns5',
        'blackrock_2_1/l101210-001.nev',
        'blackrock_2_1/l101210-001-02.nev']

    @unittest.skipUnless(HAVE_SCIPY, "requires scipy")
    def test_compare_blackrockio_with_matlabloader(self):
        """
        This test compares the output of ReachGraspIO.read_block() with the
        output generated by a Matlab implementation of a Blackrock file reader
        provided by the company. The output for comparison is provided in a
        .mat file created by the script create_data_matlab_blackrock.m.
        The function tests LFPs, spike times, and digital events on channels
        80-83 and spike waveforms on channel 82, unit 1.
        For details on the file contents, refer to FileSpec2.3.txt

        Ported to the rawio API by Samuel Garcia.
        """

        # Load data from Matlab generated files
        ml = scipy.io.loadmat(self.get_filename_path('FileSpec2.3001.mat'))

        lfp_ml = ml['lfp']  # (channel x time) LFP matrix
        ts_ml = ml['ts']  # spike time stamps
        elec_ml = ml['el']  # spike electrodes
        unit_ml = ml['un']  # spike unit IDs
        wf_ml = ml['wf']  # waveform unit 1 channel 1
        mts_ml = ml['mts']  # marker time stamps
        mid_ml = ml['mid']  # marker IDs

        # Load data in channels 1-3 from original data files using the Neo
        # BlackrockIO
        reader = BlackrockRawIO(filename=self.get_filename_path('FileSpec2.3001'))
        reader.parse_header()

        # Check if analog data on channels 1-8 are equal
        self.assertGreater(reader.signal_channels_count(), 0)
        for c in range(0, 8):
            raw_sigs = reader.get_analogsignal_chunk(channel_indexes=[c])
            raw_sigs = raw_sigs.flatten()
            assert_equal(raw_sigs[:-1], lfp_ml[c, :])

        # Check if spikes in channels are equal
        nb_unit = reader.unit_channels_count()
        for unit_index in range(nb_unit):
            unit_name = reader.header['unit_channels'][unit_index]['name']
            # name is chXX#YY where XX is channel_id and YY is unit_id
            channel_id, unit_id = unit_name.split('#')
            channel_id = int(channel_id.replace('ch', ''))
            unit_id = int(unit_id)

            matlab_spikes = ts_ml[(elec_ml == channel_id) & (unit_ml == unit_id)]

            io_spikes = reader.get_spike_timestamps(unit_index=unit_index)
            assert_equal(io_spikes, matlab_spikes)

            # Check waveforms of channel 1, unit 0
            if channel_id == 1 and unit_id == 0:
                io_waveforms = reader.get_spike_raw_waveforms(unit_index=unit_index)
                io_waveforms = io_waveforms[:, 0, :]  # remove dim 1
                assert_equal(io_waveforms, wf_ml)

        # Check if digital input port events are equal
        nb_ev_chan = reader.event_channels_count()
        # ~ print(reader.header['event_channels'])
        for ev_chan in range(nb_ev_chan):
            name = reader.header['event_channels']['name'][ev_chan]
            # ~ print(name)
            all_timestamps, _, labels = reader.get_event_timestamps(
                event_channel_index=ev_chan)
            if name == 'digital_input_port':
                for label in np.unique(labels):
                    python_digievents = all_timestamps[labels == label]
                    matlab_digievents = mts_ml[mid_ml == int(label)]
                    assert_equal(python_digievents, matlab_digievents)
            elif name == 'comments':
                pass
                # TODO: Save comments to Matlab file.

    @unittest.skipUnless(HAVE_SCIPY, "requires scipy")
    def test_compare_blackrockio_with_matlabloader_v21(self):
        """
        This test compares the output of ReachGraspIO.read_block() with the
        output generated by a Matlab implementation of a Blackrock file reader
        provided by the company. The output for comparison is provided in a
        .mat file created by the script create_data_matlab_blackrock.m.
        The function tests LFPs, spike times, and digital events.

        Ported to the rawio API by Samuel Garcia.
        """

        dirname = self.get_filename_path('blackrock_2_1/l101210-001')
        # First run with parameters for ns5, then run with correct parameters for ns2
        parameters = [('blackrock_2_1/l101210-001_nev-02_ns5.mat',
                       {'nsx_to_load': 5, 'nev_override': '-'.join([dirname, '02'])}, 96),
                      ('blackrock_2_1/l101210-001.mat', {'nsx_to_load': 2}, 6)]
        for param in parameters:
            # Load data from Matlab generated files
            ml = scipy.io.loadmat(self.get_filename_path(filename=param[0]))
            lfp_ml = ml['lfp']  # (channel x time) LFP matrix
            ts_ml = ml['ts']  # spike time stamps
            elec_ml = ml['el']  # spike electrodes
            unit_ml = ml['un']  # spike unit IDs
            wf_ml = ml['wf']  # waveforms
            mts_ml = ml['mts']  # marker time stamps
            mid_ml = ml['mid']  # marker IDs

            # Load data from original data files using the Neo BlackrockIO
            reader = BlackrockRawIO(dirname, **param[1])
            reader.parse_header()

            # Check if analog data are equal
            self.assertGreater(reader.signal_channels_count(), 0)

            for c in range(0, param[2]):
                raw_sigs = reader.get_analogsignal_chunk(channel_indexes=[c])
                raw_sigs = raw_sigs.flatten()
                assert_equal(raw_sigs[:], lfp_ml[c, :])

            # Check if spikes in channels are equal
            nb_unit = reader.unit_channels_count()
            for unit_index in range(nb_unit):
                unit_name = reader.header['unit_channels'][unit_index]['name']
                # name is chXX#YY where XX is channel_id and YY is unit_id
                channel_id, unit_id = unit_name.split('#')
                channel_id = int(channel_id.replace('ch', ''))
                unit_id = int(unit_id)

                matlab_spikes = ts_ml[(elec_ml == channel_id) & (unit_ml == unit_id)]

                io_spikes = reader.get_spike_timestamps(unit_index=unit_index)
                assert_equal(io_spikes, matlab_spikes)

                # Check all waveforms
                io_waveforms = reader.get_spike_raw_waveforms(unit_index=unit_index)
                io_waveforms = io_waveforms[:, 0, :]  # remove dim 1
                matlab_wf = wf_ml[np.nonzero(
                    np.logical_and(elec_ml == channel_id, unit_ml == unit_id)), :][0]
                assert_equal(io_waveforms, matlab_wf)

            # Check if digital input port events are equal
            nb_ev_chan = reader.event_channels_count()
            # ~ print(reader.header['event_channels'])
            for ev_chan in range(nb_ev_chan):
                name = reader.header['event_channels']['name'][ev_chan]
                # ~ print(name)
                if name == 'digital_input_port':
                    all_timestamps, _, labels = reader.get_event_timestamps(
                        event_channel_index=ev_chan)

                    for label in np.unique(labels):
                        python_digievents = all_timestamps[labels == label]
                        matlab_digievents = mts_ml[mid_ml == int(label)]
                        assert_equal(python_digievents, matlab_digievents)


if __name__ == '__main__':
    unittest.main()
