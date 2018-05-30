import pytest
import wave
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




def test_remote_noise_generator():
    # for sample in sound.remote_noise_generator(10):
    pass
