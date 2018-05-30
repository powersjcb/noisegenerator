from unittest import mock
import wave

import pytest
from . import sound


@pytest.fixture
def noise_file(tmpdir):
    filename = f'{tmpdir}/random_sound.wav'
    sound.write_wav(
        filename,
        sound.native_noise_generator)
    return filename


@pytest.fixture
def external_noise_file(tmpdir):
    filename = f'{tmpdir}/random_sound.wav'
    sound.write_wav(
        filename,
        sound.remote_noise_generator)
    return filename


def test_randomly_generated_sound(noise_file):
    with wave.open(noise_file, 'r') as w:
        frames = w.getnframes()
        framerate = w.getframerate()

        # test file has 3 second duration
        assert int(frames / framerate) == 3

        # assert that not all values are identical
        data = w.readframes(frames)
        assert not all(d == data[0] for d in data)


@mock.patch('requests.get')
def test_remote_noise_valid_response(get):
    res = mock.MagicMock()
    res.status_code = 200
    res.content = b'1\n2\n\n'
    get.return_value = res
    assert [1, 2] == [s for s in sound.remote_noise_generator(2)]


@mock.patch('requests.get')
def test_remote_noise_throttled(get):
    res = mock.MagicMock()
    res.status_code = 503
    res.content = b'too many requests'
    get.return_value = res

    with pytest.raises(Exception):
        assert not [s for s in sound.remote_noise_generator(2)]
