""" Unit tests for PyLive """

import pytest
import time
import live

from tests.shared import open_test_set

def setup_module():
    open_test_set()

@pytest.fixture(scope="module")
def track():
    set = live.Set()
    set.scan(scan_devices = True)
    set.tracks[1].stop()
    time.sleep(0.1)
    return set.tracks[1]

def test_track_get_clips(track):
    assert len(track.clips) == 5

def test_track_get_active_clips(track):
    assert len(track.active_clips) == 4

def test_track_get_devices(track):
    assert len(track.devices) == 1

def test_track_scene_indexes(track):
    scene_indexes = track.scene_indexes
    assert scene_indexes == [ 0, 1, 2, 4 ]

def test_track_states(track):
    # is_stopped
    # is_starting
    # is_playing
    track.set.quantization = 5
    assert track.is_stopped
    track.set.play()
    time.sleep(0.1)
    track.clips[0].play()
    time.sleep(0.2)
    assert track.is_starting
    time.sleep(1.0)
    assert track.is_playing
    track.stop()
    time.sleep(1.0)
    assert track.is_stopped
    track.set.stop()

def test_track_stop(track):
    track.set.quantization = 0
    time.sleep(0.1)
    track.clips[0].play()
    time.sleep(0.2)
    assert track.is_playing
    track.stop()
    time.sleep(0.2)
    assert track.is_stopped

def test_track_scan_clip_names(track):
    assert track.clips[0].name is None
    track.scan_clip_names()
    assert track.active_clips[0].name == "one"
    assert track.active_clips[1].name == "two"
    assert track.active_clips[2].name == "three"
    assert track.active_clips[3].name == "four"

def test_track_volume(track):
    assert track.volume == pytest.approx(0.85)
    track.volume = 0.0
    assert track.volume == 0.0
    track.volume = 0.85

def test_track_pan(track):
    assert track.pan == 0
    track.pan = 1
    assert track.pan == 1
    track.pan = 0

def test_track_mute(track):
    assert track.mute == 0
    track.mute = 1
    assert track.mute == 1
    track.mute = 0

def test_track_arm(track):
    assert track.arm == 0
    track.arm = 1
    assert track.arm == 1
    track.arm = 0

def test_track_solo(track):
    assert track.solo == 0
    track.solo = 1
    assert track.solo == 1
    track.solo = 0

def test_track_send(track):
    assert track.get_send(0) == pytest.approx(0.0)
    track.set_send(0, 1.0)
    assert track.get_send(0) == 1.0
    track.set_send(0, 0.0)

def test_track_device_named(track):
    device = track.get_device_named("Operator")
    assert device is not None
    assert device == track.devices[0]
