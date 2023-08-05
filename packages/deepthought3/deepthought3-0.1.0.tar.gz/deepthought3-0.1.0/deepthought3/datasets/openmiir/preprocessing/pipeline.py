__author__ = "sstober"

import logging

log = logging.getLogger(__name__)

import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import mne
from mne.io import read_raw_edf
from mne.channels import rename_channels, make_standard_montage
from mne.preprocessing import ICA, read_ica
from mne.viz.topomap import plot_topomap
from mne import pick_types

import deepthought3
from deepthought3.util.fs_util import ensure_parent_dir_exists
from deepthought3.util.logging_util import configure_custom
from deepthought3.datasets.eeg.biosemi64 import Biosemi64Layout
from deepthought3.datasets.openmiir.eeg import recording_has_mastoid_channels
from deepthought3.datasets.openmiir.events import decode_event_id
from deepthought3.datasets.openmiir.preprocessing.events import (
    merge_trial_and_audio_onsets,
    generate_beat_events,
    simple_beat_event_id_generator,
    extract_events_from_raw,
)
from deepthought3.datasets.openmiir.metadata import (
    get_stimuli_version,
    load_stimuli_metadata,
)
from deepthought3.mneext.viz import plot_ica_overlay_evoked
from deepthought3.mneext.resample import fast_resample_mne

RAW_EOG_CHANNELS = ["EXG1", "EXG2", "EXG3", "EXG4"]
MASTOID_CHANNELS = ["EXG5", "EXG6"]


def load_raw_info(subject, mne_data_root=None, verbose=False):

    if mne_data_root is None:
        # use default data root
        import deepthought3

        data_root = os.path.join(deepthought3.DATA_PATH, "OpenMIIR")
        mne_data_root = os.path.join(data_root, "eeg", "mne")

    mne_data_filepath = os.path.join(mne_data_root, "{}-raw.fif".format(subject))

    log.info(
        'Loading raw data info for subject "{}" from {}'.format(
            subject, mne_data_filepath
        )
    )
    raw = mne.io.Raw(mne_data_filepath, preload=False, verbose=verbose)
    return raw.info


def load_raw(subject, **args):
    return _load_raw(
        subject=subject, has_mastoid_channels=recording_has_mastoid_channels, **args
    )


def _load_raw(
    subject,
    mne_data_root=None,
    verbose=False,
    onsets=None,
    interpolate_bad_channels=False,
    has_mastoid_channels=None,  # None=True, False, or callable(subject) returning True/False
    apply_reference=True,  # by default, reference the data
    reference_mastoids=True,
):

    if mne_data_root is None:
        # use default data root
        import deepthought3

        data_root = os.path.join(deepthought3.DATA_PATH, "OpenMIIR")
        mne_data_root = os.path.join(data_root, "eeg", "mne")

    mne_data_filepath = os.path.join(mne_data_root, "{}-raw.fif".format(subject))

    log.info(
        'Loading raw data for subject "{}" from {}'.format(subject, mne_data_filepath)
    )
    raw = mne.io.Raw(mne_data_filepath, preload=True, verbose=verbose)

    if apply_reference:
        if (
            has_mastoid_channels is None
            or has_mastoid_channels is True
            or has_mastoid_channels(subject) is True
        ):
            ## referencing to mastoids
            if reference_mastoids:
                log.info("Referencing to mastoid channels: {}".format(MASTOID_CHANNELS))
                mne.io.set_eeg_reference(raw, MASTOID_CHANNELS, copy=False)  # inplace
            else:
                log.info(
                    "This recording has unused mastoid channels: {} "
                    "To use them, re-run with reference_mastoids=True.".format(
                        MASTOID_CHANNELS
                    )
                )
            raw.drop_channels(MASTOID_CHANNELS)
        else:
            ## referencing to average
            log.info("Referencing to average.")
            mne.io.set_eeg_reference(raw, copy=False)

    ## optional event merging
    if onsets == "audio":
        merge_trial_and_audio_onsets(
            raw,
            use_audio_onsets=True,
            inplace=True,
            stim_channel="STI 014",
            verbose=verbose,
        )
    elif onsets == "trials":
        merge_trial_and_audio_onsets(
            raw,
            use_audio_onsets=True,
            inplace=True,
            stim_channel="STI 014",
            verbose=verbose,
        )
    # else: keep both

    # add digitization
    raw.set_montage(Biosemi64Layout().as_montage())

    bads = raw.info["bads"]
    if bads is not None and len(bads) > 0:
        if interpolate_bad_channels:
            log.info("Interpolating bad channels: {}".format(bads))
            raw.interpolate_bads()
        else:
            log.info(
                "This file contains some EEG channels marked as bad: {}\n"
                "To interpolate bad channels run load_raw() with interpolate_bad_channels=True."
                "".format(bads)
            )

    return raw


def interpolate_bad_channels(inst):
    bads = inst.info["bads"]
    if bads is not None and len(bads) > 0:
        log.info("Interpolating bad channels...")
        inst.interpolate_bads()
    else:
        log.info("No channels marked as bad. Nothing to interpolate.")


def load_ica(subject, description, ica_data_root=None):
    if ica_data_root is None:
        # use default data root
        import deepthought3

        data_root = os.path.join(deepthought3.DATA_PATH, "OpenMIIR")
        ica_data_root = os.path.join(data_root, "eeg", "preprocessing", "ica")

    ica_filepath = os.path.join(
        ica_data_root, "{}-{}-ica.fif".format(subject, description)
    )
    return read_ica(ica_filepath)


def import_and_process_metadata(
    biosemi_data_root, mne_data_root, subject, verbose=True, overwrite=False
):

    ## check whether output already exists
    output_filepath = os.path.join(mne_data_root, "{}-raw.fif".format(subject))

    if os.path.exists(output_filepath):
        if not overwrite:
            log.info("Skipping existing {}".format(output_filepath))
            return

    ## import raw BDF file from biosemi
    bdf_filepath = os.path.join(biosemi_data_root, "{}.bdf".format(subject))

    ## NOTE: marks EXT1-4 channels as EOG channels during import
    log.info("Importing raw BDF data from: {}".format(bdf_filepath))
    raw = read_raw_edf(
        bdf_filepath, eog=RAW_EOG_CHANNELS, preload=True, verbose=verbose
    )
    log.info("Imported raw data: {}".format(raw))

    sfreq = raw.info["sfreq"]
    if sfreq != 512:
        log.warn("Unexpected sample rate: {} Hz".format(sfreq))
        log.warn("Re-sampling to 512 Hz")
        fast_resample_mne(
            raw, 512, res_type="sinc_best", preserve_events=True, verbose=True
        )

    ## mark all unused channels as bad
    raw.info["bads"] += [
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8",
        "C9",
        "C10",
        "C11",
        "C12",
        "C13",
        "C14",
        "C15",
        "C16",
        "C17",
        "C18",
        "C19",
        "C20",
        "C21",
        "C22",
        "C23",
        "C24",
        "C25",
        "C26",
        "C27",
        "C28",
        "C29",
        "C30",
        "C31",
        "C32",
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "D6",
        "D7",
        "D8",
        "D9",
        "D10",
        "D11",
        "D12",
        "D13",
        "D14",
        "D15",
        "D16",
        "D17",
        "D18",
        "D19",
        "D20",
        "D21",
        "D22",
        "D23",
        "D24",
        "D25",
        "D26",
        "D27",
        "D28",
        "D29",
        "D30",
        "D31",
        "D32",
        "E1",
        "E2",
        "E3",
        "E4",
        "E5",
        "E6",
        "E7",
        "E8",
        "E9",
        "E10",
        "E11",
        "E12",
        "E13",
        "E14",
        "E15",
        "E16",
        "E17",
        "E18",
        "E19",
        "E20",
        "E21",
        "E22",
        "E23",
        "E24",
        "E25",
        "E26",
        "E27",
        "E28",
        "E29",
        "E30",
        "E31",
        "E32",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "F13",
        "F14",
        "F15",
        "F16",
        "F17",
        "F18",
        "F19",
        "F20",
        "F21",
        "F22",
        "F23",
        "F24",
        "F25",
        "F26",
        "F27",
        "F28",
        "F29",
        "F30",
        "F31",
        "F32",
        "G1",
        "G2",
        "G3",
        "G4",
        "G5",
        "G6",
        "G7",
        "G8",
        "G9",
        "G10",
        "G11",
        "G12",
        "G13",
        "G14",
        "G15",
        "G16",
        "G17",
        "G18",
        "G19",
        "G20",
        "G21",
        "G22",
        "G23",
        "G24",
        "G25",
        "G26",
        "G27",
        "G28",
        "G29",
        "G30",
        "G31",
        "G32",
        "H1",
        "H2",
        "H3",
        "H4",
        "H5",
        "H6",
        "H7",
        "H8",
        "H9",
        "H10",
        "H11",
        "H12",
        "H13",
        "H14",
        "H15",
        "H16",
        "H17",
        "H18",
        "H19",
        "H20",
        "H21",
        "H22",
        "H23",
        "H24",
        "H25",
        "H26",
        "H27",
        "H28",
        "H29",
        "H30",
        "H31",
        "H32",
        "EXG7",
        "EXG8",
        "GSR1",
        "GSR2",
        "Erg1",
        "Erg2",
        "Resp",
        "Plet",
        "Temp",
    ]
    log.info("Marked unused channels as bad: {}".format(raw.info["bads"]))

    if not recording_has_mastoid_channels(subject):
        raw.info["bads"] += ["EXG5", "EXG6"]

    picks = mne.pick_types(
        raw.info, meg=False, eeg=True, eog=True, stim=True, exclude="bads"
    )

    ## process events
    markers_filepath = os.path.join(
        biosemi_data_root, "{}_EEG_Data.mat".format(subject)
    )
    log.info("Processing events, external source: {}".format(markers_filepath))
    events = extract_events_from_raw(raw, markers_filepath, subject, verbose)
    raw._data[-1, :].fill(0)  # delete data in stim channel
    raw.add_events(events)

    # crop to first event - 1s ... last event + 20s (longer than longest trial)
    onesec = raw.info["sfreq"]
    tmin, tmax = raw.times[[events[0, 0] - onesec, events[-1, 0] + 20 * onesec]]
    log.info("Cropping raw inplace to {:.3f}s - {:.3f}s".format(tmin, tmax))
    raw.crop(tmin=tmin, tmax=tmax, copy=False)
    # fix sample offser -> 0
    raw.last_samp -= raw.first_samp
    raw.first_samp = 0

    ensure_parent_dir_exists(output_filepath)
    log.info("Saving raw fif data to: {}".format(output_filepath))
    raw.save(output_filepath, picks=picks, overwrite=overwrite, verbose=False)

    del raw

    raw = fix_channel_infos(output_filepath, verbose=verbose)

    log.info("Imported {}".format(raw))
    log.info("Metadata: {}".format(raw.info))


def fix_channel_infos(mne_data_filepath, verbose=True):

    log.info("Loading raw fif data from: {}".format(mne_data_filepath))
    raw = mne.io.Raw(mne_data_filepath, preload=True, verbose=verbose)

    raw.info["bads"] = []  # reset bad channels as they have been removed already

    montage = Biosemi64Layout().as_montage()
    log.info("Applying channel montage: {}".format(montage))

    ## change EEG channel names
    mapping = dict()
    bdf_channel_names = raw.ch_names
    for i, channel_name in enumerate(montage.ch_names):
        log.debug(
            "renaming channel {}: {} -> {}".format(
                i, bdf_channel_names[i], channel_name
            )
        )
        mapping[bdf_channel_names[i]] = channel_name
    rename_channels(raw.info, mapping)

    # mne.channels.apply_montage(raw.info, montage) # in mne 0.9
    raw.set_montage(montage)  # in mne 0.9
    log.info("Saving raw fif data to: {}".format(mne_data_filepath))
    raw.save(mne_data_filepath, overwrite=True, verbose=False)

    return raw


def clean_data(mne_data_root, subject, verbose=True, overwrite=False):

    ## check whether output already exists
    output_filepath = os.path.join(mne_data_root, "{}_filtered-raw.fif".format(subject))

    if os.path.exists(output_filepath):
        if not overwrite:
            log.info("Skipping existing {}".format(output_filepath))
            return

    input_filepath = os.path.join(mne_data_root, "{}-raw.fif".format(subject))

    raw = mne.io.Raw(input_filepath, preload=True, verbose=verbose)

    ## apply bandpass filter
    raw.filter(
        0.5,
        30,
        filter_length="10s",
        l_trans_bandwidth=0.1,
        h_trans_bandwidth=0.5,
        method="fft",
        iir_params=None,
        picks=None,
        n_jobs=1,
        verbose=verbose,
    )

    ensure_parent_dir_exists(output_filepath)
    raw.save(output_filepath, overwrite=overwrite, verbose=False)


class Pipeline(object):
    """
    Aux-object bundling import/pre-processing functions
    for usage in ipython notebook

    This has to be understood as on workflow (with breaks for decisions)
    to be run in the given order
    """

    def __init__(self, subject, settings=dict()):
        self.subject = subject
        self.settings = settings

        if "debug" in settings:
            configure_custom(settings["debug"])
        else:
            configure_custom(debug=True)

        if "mne_log_level" in settings:
            mne.set_log_level(settings["mne_log_level"])
        else:
            mne.set_log_level("INFO")

        if "sfreq" in settings:
            self.downsample_sfreq = settings["sfreq"]
        else:
            self.downsample_sfreq = 64

        if "layout" in settings:
            self.layout = settings["layout"]
        else:
            self.layout = mne.channels.read_layout("biosemi.lay")

        if "data_root" in settings:
            self.data_root = settings["data_root"]
        else:
            self.data_root = os.path.join(deepthought3.DATA_PATH, "OpenMIIR")

        # load stimuli metadata version
        self.stimuli_version = get_stimuli_version(subject)

        # initial state
        self.raw = None
        self.ica = None

        self.filtered = False
        self.downsampled = False

    def import_and_process_metadata(self, verbose=None, overwrite=False):

        biosemi_data_root = os.path.join(self.data_root, "eeg", "biosemi")
        mne_data_root = os.path.join(self.data_root, "eeg", "mne")

        import_and_process_metadata(
            biosemi_data_root,
            mne_data_root,
            self.subject,
            verbose=verbose,
            overwrite=overwrite,
        )

    def load_raw(
        self, verbose=None, interpolate_bad_channels=False, reference_mastoids=True
    ):
        # if "has_subfolders" in self.settings and self.settings["has_subfolders"]:
        #     mne_data_root = os.path.join(self.data_root, "eeg", "mne")
        # else:
        #     mne_data_root = self.data_root
        mne_data_root = os.path.join(self.data_root, "eeg", "mne")

        self.raw = load_raw(
            self.subject,
            mne_data_root=mne_data_root,
            interpolate_bad_channels=interpolate_bad_channels,
            reference_mastoids=reference_mastoids,
            verbose=verbose,
        )
        self.eeg_picks = mne.pick_types(
            self.raw.info, meg=False, eeg=True, eog=False, stim=False, exclude=[]
        )

        self.filtered = False
        self.downsampled = False

    def plot_raw(self):

        try:
            print('scroll using cursor keys, click on channels to mark as "bad"')
            color = dict(eeg="blue", eog="red", stim="green")
            self.raw.plot(n_channels=69, remove_dc=True, color=color)
        except:
            print("ERROR: interactive mode required.")

    def print_bad_channels(self):
        print("bad channels:", self.raw.info["bads"])

    def reset_bad_channels(self):
        self.raw.info["bads"] = []

    def mark_bad_channels(self, bads=None, save_to_raw=False):
        old_bads = self.raw.info["bads"]

        if bads is None:
            bads = old_bads

        # check whether some old bad channels are not in the new list
        for bad in self.raw.info["bads"]:
            if not bad in bads:
                log.warn(
                    "Channel {} was earlier marked as bad but is not in the new list. "
                    "Please reload the raw data and reset the bad channel list "
                    "using reset_bad_channels() "
                    "or add the channel to the new list!".format(bad)
                )
                return

        # if len(bads) == 0:
        #     print 'No bad channels rejected.'

        self.raw.info["bads"] = bads

        print("The following channels have been marked as bad:", self.raw.info["bads"])

        if save_to_raw:
            # raw needs to be reloaded for this with the mastoid channels still present
            mne_data_root = os.path.join(self.data_root, "eeg", "mne")
            tmp = load_raw(
                self.subject,
                mne_data_root=mne_data_root,
                interpolate_bad_channels=False,
                reference_mastoids=False,
            )
            tmp.info["bads"] = bads

            mne_data_filepath = os.path.join(
                mne_data_root, "{}-raw.fif".format(self.subject)
            )
            log.info(
                "Updating bad channel information in: {}".format(mne_data_filepath)
            )
            tmp.save(mne_data_filepath, overwrite=True, verbose=False)

    def interpolate_bad_channels(self):
        if len(self.raw.info["bads"]) > 0:
            log.warn(
                "The following channels are interpolated: {}. "
                "This overwrites the channel data. "
                "To undo this, the raw data needs to be reloaded.".format(
                    self.raw.info["bads"]
                )
            )
            self.raw.interpolate_bads()
        else:
            print("No bad channels that need to be interpolated.")

    def plot_bad_channel_topo(self):
        bads = [self.raw.ch_names.index(ch) for ch in self.raw.info["bads"]]
        # print bads

        # topo = np.zeros((64), dtype=float)
        topo = self.raw[0:64, 0][0].squeeze()
        # print topo.shape

        mask = np.zeros(64, dtype=bool)
        mask[bads] = True
        mask_params = dict(marker="", markeredgecolor="r", linewidth=0, markersize=4)

        layout = Biosemi64Layout()
        pos = layout.projected_xy_coords()

        # print pos.shape
        plt.figure(figsize=(5, 5))
        mne.viz.plot_topomap(
            topo,
            pos,
            res=2,
            sensors="k.",
            names=layout.channel_names(),
            show_names=True,
            cmap="RdBu_r",
            vmin=-1,
            vmax=1,
            #                              vmin=vmin, vmax=vmax,
            axis=plt.gca(),
            contours=False,
            mask=mask,
            mask_params=mask_params,
        )

    ## check the trial events
    def check_trial_events(self, verbose=False):

        # assert self.filtered is False
        assert self.downsampled is False

        raw = self.raw

        trial_events = mne.find_events(raw, stim_channel="STI 014", shortest_event=0)

        if verbose:
            print(trial_events)

        plt.figure(figsize=(17, 10))
        axes = plt.gca()
        mne.viz.plot_events(trial_events, raw.info["sfreq"], raw.first_samp, axes=axes)
        print("1st event at ", raw.times[trial_events[0, 0]])
        print("last event at ", raw.times[trial_events[-1, 0]])
        trial_event_times = raw.times[trial_events[:, 0]]

        self.trial_events = trial_events
        self.trial_event_times = trial_event_times

    def check_trial_audio_onset_merge(self, use_audio_onsets=True, verbose=None):

        # assert self.filtered is False
        assert self.downsampled is False
        raw = self.raw

        ## check whether trial and audio events are merged correctly
        merged_events = merge_trial_and_audio_onsets(
            raw, use_audio_onsets=use_audio_onsets, inplace=False
        )
        if verbose:
            for event in merged_events:
                print(event)

        plt.figure(figsize=(17, 10))
        axes = plt.gca()
        mne.viz.plot_events(merged_events, raw.info["sfreq"], raw.first_samp, axes=axes)

    def merge_trial_and_audio_onsets(self, use_audio_onsets=True):
        raw = self.raw

        # save original events
        self.orig_trial_events = self.trial_events

        # merge
        merge_trial_and_audio_onsets(
            raw, use_audio_onsets=use_audio_onsets, inplace=True
        )

        # recompute trial_events and times
        trial_events = mne.find_events(raw, stim_channel="STI 014", shortest_event=0)
        trial_event_times = raw.times[trial_events[:, 0]]

        self.trial_events = trial_events
        self.trial_event_times = trial_event_times

    def check_trial_event_consistency(self):
        meta = load_stimuli_metadata(self.data_root, self.stimuli_version)
        sfreq = self.raw.info["sfreq"]
        n_errors = 0
        for i, event in enumerate(self.trial_events[:-1]):
            event_id = event[2]
            start = event[0]
            if event_id < 1000:
                stim_id, cond = decode_event_id(event_id)
                if cond in [1, 2]:
                    field = "length_with_cue"
                else:
                    field = "length_without_cue"
                sample_len = sfreq * meta[stim_id][field]
            else:
                sample_len = 1

            next_start = self.trial_events[i + 1, 0]

            if next_start < start + sample_len:
                expected_len = sample_len / float(sfreq)
                event_len = (next_start - start) / float(sfreq)
                log.warn(
                    "warning: event {} starts before expected end of {}".format(
                        self.trial_events[i + 1], event
                    )
                )
                log.warn(
                    "expected length: {:.3f}s, real length: {:.3f}s, delta: {:.3f}s".format(
                        expected_len, event_len, expected_len - event_len
                    )
                )
                n_errors += 1
        log.info("{} problems detected.".format(n_errors))

    def check_psd(self, fmax=None, average=True):

        raw = self.raw

        ## check PSD
        # plot PSD of raw data
        if fmax is None:
            fmax = raw.info["sfreq"]
        plt.figure(figsize=(17, 5))
        axes = plt.gca()
        raw.plot_psd(
            average=average,
            area_mode="range",
            tmax=10.0,
            ax=axes,
            picks=self.eeg_picks,
            fmax=fmax,
        )

    def check_channel(self, ch_num):
        raw = self.raw

        ## have a look at 1st channel
        channel = raw[ch_num, :][0].squeeze()
        print(channel.shape)
        plt.figure(figsize=(17, 4))
        plt.plot(channel)

    ###################### bandpass filtering - this will change raw ######################

    def bandpass_filter(self):

        raw = self.raw

        ## apply bandpass filter, use 4 processes to speed things up
        raw.filter(
            0.5,
            30,
            picks=self.eeg_picks,
            filter_length="10s",
            l_trans_bandwidth=0.5,
            h_trans_bandwidth=0.5,
            method="fft",
            n_jobs=4,
            verbose=True,
        )

        self.filtered = True

    ## generate events epochs after bandpass !

    def generate_beat_events(self, verbose=None):

        assert self.filtered is True
        assert self.downsampled is False
        raw = self.raw

        ## generate beat events and epochs before downsampling
        # read trial events

        if hasattr(self, "trial_events"):
            trial_events = self.trial_events
        else:
            trial_events = mne.find_events(
                raw, stim_channel="STI 014", shortest_event=0
            )

        # print(trial_events)
        # generate simple beat events with same ID (10000)
        beat_events = generate_beat_events(
            trial_events,
            version=self.stimuli_version,
            beat_event_id_generator=simple_beat_event_id_generator,
            verbose=verbose,
        )

        # FIXME: read from settings
        picks = mne.pick_types(
            raw.info, meg=False, eeg=True, eog=True, stim=True, exclude=[]
        )
        event_id = None  # any
        tmin = -0.2  # start of each epoch (200ms before the trigger)
        tmax = 0.8  # end of each epoch (600ms after the trigger) - longest beat is 0.57s long
        detrend = 0  # remove dc
        # reject = dict(eog=250e-6) # TODO: optionally reject epochs
        beat_epochs = mne.Epochs(
            raw,
            beat_events,
            event_id,
            tmin,
            tmax,
            preload=True,
            proj=False,
            picks=picks,
            verbose=False,
        )
        print(beat_epochs)

        self.beat_epochs = beat_epochs

    # ## compute EOG epochs before downsampling
    def find_eog_events(self, verbose=None):

        assert self.filtered is True
        assert self.downsampled is False
        raw = self.raw

        # check for EOG artifacts:
        # NOTE: this should NOT be done after resampling!
        eog_event_id = 5000
        eog_events = mne.preprocessing.find_eog_events(raw, eog_event_id)

        plt.figure(figsize=(17, 0.5))
        axes = plt.gca()
        mne.viz.plot_events(eog_events, raw.info["sfreq"], raw.first_samp, axes=axes)

        # create epochs around EOG events
        picks = mne.pick_types(
            raw.info, meg=False, eeg=True, eog=True, stim=True, exclude=[]
        )  # FIXME
        tmin = -0.5
        tmax = 0.5
        eog_epochs = mne.Epochs(
            raw,
            events=eog_events,
            event_id=eog_event_id,
            tmin=tmin,
            tmax=tmax,
            proj=False,
            picks=picks,
            preload=True,
            verbose=False,
        )

        self.eog_events = eog_events
        self.eog_epochs = eog_epochs

    ###################### down-sampling - this will change raw ######################

    def downsample(self):
        raw = self.raw
        sfreq = self.downsample_sfreq

        print(
            """
        from doc:
        WARNING: The intended purpose of this function is primarily to speed
                up computations (e.g., projection calculation) when precise timing
                of events is not required, as downsampling raw data effectively
                jitters trigger timings. It is generally recommended not to epoch
                downsampled data, but instead epoch and then downsample, as epoching
                downsampled data jitters triggers.

        NOTE: event onset collisions will be reported as warnings
              in that case, it might be a good idea to pick either the trial onset or audio onset events
              and delete the other ones before downsampling
        """
        )

        print("down-sampling raw and events stim channel ...")
        fast_resample_mne(
            raw, sfreq, res_type="sinc_best", preserve_events=True, verbose=True
        )
        # fast_resample_mne(raw, sfreq, res_type='sinc_fastest', preserve_events=True, verbose=False)
        # stim_picks = pick_types(
        #     self.info, meg=False, ref_meg=False, stim=True, exclude=[]
        # )
        # stim_picks = np.asanyarray(stim_picks)
        # self.raw.resample(
        #     sfreq,
        #     stim_picks=stim_picks
        # )

        # resample epochs
        print("down-sampling epochs ...")
        self.eog_epochs.resample(sfreq)
        self._downsample_epochs()

        print("TODO: down-sampling events (not in stim channel) ...")
        # TODO: resample events

        self.downsampled = True

    def _downsample_epochs(self):
        sfreq = self.downsample_sfreq
        self.beat_epochs.resample(sfreq)

    def check_resampled_trial_events(self, plot=True, verbose=None):

        assert self.downsampled is True
        raw = self.raw
        trial_event_times = self.trial_event_times

        resampled_trial_events = mne.find_events(
            raw, stim_channel="STI 014", shortest_event=0
        )
        # print resampled_trial_events

        if plot:
            plt.figure(figsize=(17, 10))
            axes = plt.gca()
            mne.viz.plot_events(
                resampled_trial_events, raw.info["sfreq"], raw.first_samp, axes=axes
            )  # , color=color, event_id=event_id)

        resampled_trial_event_times = raw.times[resampled_trial_events[:, 0]]
        # print resampled_trial_event_times

        diff = resampled_trial_event_times - trial_event_times
        print(
            "event onset jitter (min, mean, max):", diff.min(), diff.mean(), diff.max()
        )
        diff = np.asarray(diff * 1000, dtype=int)

        if verbose:
            for i, event in enumerate(resampled_trial_events):
                print(event, diff[i])

    ############################ ICA aux functions ############################

    # override to change ICA behavior
    def _get_ica_data(self):
        # return self.raw       # fit to raw data
        return self.beat_epochs  # fit to epochs

    def compute_ica(self, method="extended-infomax", random_seed=42, verbose=None):

        data = self._get_ica_data()
        random_state = np.random.RandomState(random_seed)

        ###############################################################################
        # 1) Fit ICA model using the FastICA algorithm

        # Other available choices are `infomax` or `extended-infomax`
        # We pass a float value between 0 and 1 to select n_components based on the
        # percentage of variance explained by the PCA components.

        # ica = ICA(n_components=0.95, method='fastica', random_state=random_state) # capture 95% of variance
        ica = ICA(
            n_components=1.0, method=method, random_state=random_state, verbose=verbose
        )  # capture full variance
        # ica = ICA(n_components=20, method='fastica', random_state=random_state)

        # tstep = Length of data chunks for artifact rejection in seconds.
        # ica.fit(raw, picks=eeg_picks, tstep=1.0, verbose=True)
        ica.fit(data)

        self.ica = ica

    ## aux functions to be moved to lib
    def plot_ica_components(self, picks=None, topomap_size=3.5):

        ica = self.ica

        if picks is None:
            n_components = ica.mixing_matrix_.shape[1]
            picks = list(range(n_components))
        if len(picks) == 0:
            print("nothing selected for plotting")
            return
        ica.plot_components(
            picks=picks, ch_type="eeg", title="", colorbar=True, show=False
        )
        axes = plt.gcf()
        axes.set_size_inches(
            min(len(picks), 5) * topomap_size, max(len(picks) / 5.0, 1) * topomap_size
        )
        plt.show()

    def inspect_source_psd(self, ic):
        data = self._get_ica_data()
        source = self.ica._transform_epochs(data, concatenate=True)[ic]
        sfreq = data.info["sfreq"]
        plt.figure()
        plt.psd(source, Fs=sfreq, NFFT=128, noverlap=0, pad_to=None)
        plt.show()

    ## aux function to score EEG channels by EOG correlation
    # FIXME: can this take raw OR epoch input?
    def find_eog_artifact_sources(self, plot=True, verbose=None):

        ica = self.ica
        raw = self.raw  # FIXME / epochs does not seem to work

        eog_picks = mne.pick_types(raw.info, meg=False, eeg=False, eog=True, stim=False)
        eog_inds_set = set()
        multi_scores = list()
        for ch in eog_picks:
            ch_name = raw.ch_names[ch]
            eog_inds, scores = ica.find_bads_eog(raw, str(ch_name), verbose=verbose)
            #     print eog_inds, scores
            if plot:
                ica.plot_scores(
                    scores,
                    exclude=eog_inds,
                    title="EOG artifact sources (red) for channel {}".format(ch_name),
                )

            multi_scores.append(scores)
            eog_inds_set.update(eog_inds)
        multi_scores = np.vstack(multi_scores)
        # print multi_scores.shape

        # IMPORTANT: due to a + operation meant to concatenate lists, ica.excluded and eog_inds must be lists, not ndarrays
        # see _pick_sources() in ica.py, line 1160
        eog_inds = list(eog_inds_set)
        scores = np.max(np.abs(multi_scores), axis=0).squeeze()

        print("suggested EOG artifact channels: ", eog_inds)
        print("EOG artifact component scores: ", scores[eog_inds])

        self.eog_exclude_inds = eog_inds
        self.eog_exclude_scores = scores
        self.merge_artifact_components()  # update combination

    def auto_detect_artifact_components(self):

        ica = self.ica
        data = self._get_ica_data()

        """
        data: raw, epochs or evoked
        """

        exclude_old = ica.exclude  # store old setting
        ica.exclude = []
        ica.detect_artifacts(data)
        auto_exclude = ica.exclude
        ica.exclude = exclude_old  # restore old setting

        self.auto_exclude_inds = auto_exclude
        self.merge_artifact_components()  # update combination

    ## aux function for readable one-liner code in notebook
    def merge_artifact_components(self):

        sets = list()
        if hasattr(self, "eog_exclude_inds"):
            sets.append(self.eog_exclude_inds)
        if hasattr(self, "auto_exclude_inds"):
            sets.append(self.auto_exclude_inds)

        if len(sets) == 1:
            merged = sets[0]
        else:
            print("merging", sets)
            merged = set()
            for s in sets:
                for e in s:
                    merged.add(e)
            merged = sorted(list(merged))

        self.suggested_artifact_components = merged

    # plot aggregated component scores and pick number of rejected eog components
    def select_artifact_sources(self, selection=None):
        ica = self.ica
        scores = self.eog_exclude_scores
        suggested_artifact_components = self.suggested_artifact_components

        print(
            'suggested channels to reject (selection="auto"): ',
            suggested_artifact_components,
        )

        print(
            "To change the component selection, specify select=[...] (component numbers) or select=N (top-N) and run this command again!"
        )

        if selection is None:
            selection = []
        elif selection == "auto":
            selection = suggested_artifact_components
        elif isinstance(selection, int):
            selection = np.abs(scores).argsort()[::-1][:selection]
        elif isinstance(selection, list):
            selection = selection
        else:
            print('ERROR: unsupported value for "selection":', selection)
            selection = []

        # IMPORTANT: due to a + operation meant to concatenate lists, ica.excluded and eog_inds must be lists, not ndarrays
        # see _pick_sources() in ica.py, line 1160
        selection = sorted(list(selection))
        ica.plot_scores(scores, exclude=selection, title="Artifact Component Scores")
        print("current selection:", selection)

        # self.selected_artifact_components = selection

    def exclude_ica_components(self, selection):
        print("excluding ICA components: ", selection)
        self.ica.exclude = selection

    def plot_sources(
        self, mode="data", components=None, highlight="excluded", plot_size=3
    ):
        ica = self.ica
        picks = components

        if mode == "data":
            data = self._get_ica_data()
        elif mode == "beats":
            data = self.beat_epochs
        elif mode == "eog":
            data = self.eog_epochs
        elif mode == "raw":
            data = self.raw
        else:
            print("ERROR: Unsupported mode:", mode)

        if highlight == "excluded":
            highlight = self.ica.exclude

        title = "Reconstructed Latent Sources for {}".format(mode)
        # show_picks = np.abs(scores).argsort()[::-1][:5]
        # show_picks = np.abs(scores).argsort()[::-1]
        # print show_picks

        if picks is None:
            n_components = ica.mixing_matrix_.shape[1]
            picks = list(range(n_components))
        if len(picks) == 0:
            print("nothing selected for plotting")
            return

        try:
            plt.show(block=False)
            ica.plot_sources(data, picks=picks, exclude=highlight, title="", show=True)
            print("Plotting in interactive mode. Click to view source!")
        except:
            print("NOTE: Plotting in non-interactive mode.")
            ica.plot_sources(data, picks=picks, exclude=highlight, title="", show=False)
            axes = plt.gcf()
            axes.set_size_inches(6 * plot_size, len(picks) / 6.0 * plot_size)
            plt.show()

    def inspect_ica_component(self, component, range=None):

        ica = self.ica
        raw = self.raw
        layout = self.layout

        if range == None:
            range = [None, None]
        start, stop = range

        #     print range
        #     ica.plot_sources(data, picks=[component],
        #                      title='component {}'.format(component),
        #                      start=start, stop=stop, show=False)
        #     axes = plt.gcf()
        #     axes.set_size_inches(300, 3)
        #     plt.show()

        #     ica.plot_sources(data.average(), picks=[component],
        #                      title='component {}'.format(component),
        #                      start=start, stop=stop, show=False)

        # sources = pipeline.ica._transform_epochs(pipeline.beat_epochs, concatenate=True)

        sources = ica._transform_raw(raw, start, stop)
        plt.figure(figsize=(17, 3))
        subplot_grid = gridspec.GridSpec(1, 6)
        ax = plt.subplot(subplot_grid[0])
        topodata = np.dot(
            ica.mixing_matrix_[:, component].T, ica.pca_components_[: ica.n_components_]
        )

        # this will take care of rejected channels
        data_picks, pos, merge_grads, names, _ = mne.viz.topomap._prepare_topo_plot(
            ica, "eeg", layout
        )

        mne.viz.topomap.plot_topomap(topodata.flatten(), pos, axis=ax, show=False)
        ax.text(
            0.01,
            0.99,
            "[{}]".format(component),
            transform=ax.transAxes,
            verticalalignment="top",
        )

        ax = plt.subplot(subplot_grid[1:6])
        ax.plot(sources[component, :])
        plt.subplots_adjust(wspace=0.06, hspace=0.1)
        plt.show()

    def inspect_source_epochs(
        self,
        component,
        mode="data",
        start=0,
        layout=[5, 1],
        figsize=(17, 2.2),
        vmax=None,
    ):

        ica = self.ica

        if mode == "data":
            data = self._get_ica_data()
        elif mode == "beats":
            data = self.beat_epochs
        elif mode == "eog":
            data = self.eog_epochs
        else:
            print("ERROR: unsupported mode:", mode)

        sources = ica._transform_epochs(data, concatenate=False)
        #     print sources.shape
        sources = sources[:, component, :]
        #     print sources.shape

        if vmax is None:
            ylims = sources.min(), sources.max()
        else:
            ylims = -vmax, vmax
        xlims = np.arange(sources.shape[-1])[[0, -1]]

        cols, rows = layout
        subplot_grid = gridspec.GridSpec(rows, cols)

        fig = plt.figure(figsize=figsize)
        fig.suptitle(
            "Reconstructed latent sources of ICA componet #{} for {} epochs[{}..{}]".format(
                component, mode, start, start + rows * cols
            ),
            size=14,
        )
        for r in range(rows):
            for c in range(cols):
                i = r * cols + c
                s = start + i

                ax = plt.subplot(subplot_grid[i])
                ax.plot(sources[s, :])
                ax.set_xlim(xlims)
                ax.set_ylim(ylims)
                ax.grid()
                if c > 0:
                    plt.setp(ax.get_yticklabels(), visible=False)
                if r < rows - 1:
                    plt.setp(ax.get_xticklabels(), visible=False)
                ax.text(
                    0.05,
                    0.95,
                    "[{}]".format(s),
                    transform=ax.transAxes,
                    verticalalignment="top",
                )

        # compact things
        plt.subplots_adjust(wspace=0.02, hspace=0.02)
        plt.show()

    def inspect_source(self, component, range=None):
        ica = self.ica
        data = self._get_ica_data()

        if range == None:
            range = [None, None]
        start, stop = range

        ica.plot_sources(
            data,
            picks=[component],
            title="component {}".format(component),
            start=start,
            stop=stop,
            show=False,
        )
        axes = plt.gcf()
        axes.set_size_inches(20, 3)
        plt.show()

        self.plot_ica_components(picks=[component], topomap_size=8)

    ## Assess component selection and unmixing quality
    def assess_unmixing_quality(
        self, verbose=None
    ):  # eog_evoked=None, raw=None, evoked=None, verbose=None):
        ica = self.ica
        eog_evoked = self.eog_epochs.average()
        raw = self.raw
        data = self._get_ica_data()

        if isinstance(data, mne.epochs._BaseEpochs):
            evoked = data.average()
        else:
            evoked = None

        if eog_evoked is not None:
            print("Assess impact on average EOG artifact:")
            ica.plot_sources(
                eog_evoked, exclude=ica.exclude
            )  # plot EOG sources + selection

            print("Assess cleaning of EOG epochs:")

            # Note: this method appears to be broken! Lines that should be red are drawn in black
            # ica.plot_overlay(eog_evoked, exclude=ica.exclude)

            # workaroud
            evoked_cln = ica.apply(eog_evoked, exclude=ica.exclude, copy=True)
            plot_ica_overlay_evoked(
                evoked=eog_evoked, evoked_cln=evoked_cln, title="", show=True
            )

        if raw is not None:
            print("Assess impact on raw. Check the amplitudes do not change:")
            ica.plot_overlay(raw)  # EOG artifacts remain

        if evoked is not None:
            print("Assess impact on evoked. Check the amplitudes do not change:")
            evoked_cln = ica.apply(evoked, exclude=ica.exclude, copy=True)
            plot_ica_overlay_evoked(
                evoked=evoked, evoked_cln=evoked_cln, title="", show=True
            )

    def get_ica_data_root(self):
        if "ica_data_root" in self.settings:
            return self.settings["ica_data_root"]
        else:
            return os.path.join(self.data_root, "eeg", "preprocessing", "ica")

    def save_ica(self, description):
        ica_data_root = self.get_ica_data_root()
        ica_filepath = os.path.join(
            ica_data_root, "{}-{}-ica.fif".format(self.subject, description)
        )
        ensure_parent_dir_exists(ica_filepath)
        self.ica.save(ica_filepath)

    def load_ica(self, description):
        ica_data_root = self.get_ica_data_root()
        self.ica = load_ica(self.subject, description, ica_data_root)
