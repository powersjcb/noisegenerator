import wave
import array
import random

import requests
from urllib.parse import urlencode


DURATION = 3  # seconds
FRAMERATE = 44100
SAMPLE_WIDTH = 2  # 2 bytes, 16bit audio
NUM_CHANNELS = 1


def fetch_random_org_noise():
    query = urlencode({
        'num': 10**4,
        'min': - 2 ** (SAMPLE_WIDTH / 2),
        'max': 2 ** (SAMPLE_WIDTH * 8 / 2),
        'base': '10',
        'format': 'plain',
        'col': 1,
    })
    url = f'https://www.random.org/integers/?{query}'
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f'invalid response, got status: {res.status_code}')
    return [int(v) for v in res.content.split(b'\n') if v]


def native_noise_generator(samples, _):
    i = 0
    while i < samples:
        yield random.randint(-2 ** 8, 2 ** 8)
        i += 1


def remote_noise_generator(samples, fetch_remote_noise):
    i = 0
    pool_idx = 1
    random_pool = []
    while i < samples:
        if pool_idx >= len(random_pool):
            pool_idx = 0
            random_pool = fetch_remote_noise()
        yield random_pool[pool_idx]
        i += 1
        pool_idx += 1


def write_wav(filename, audio_generator):
    with wave.open(filename, 'w') as w:
        w.setnchannels(NUM_CHANNELS)
        w.setframerate(FRAMERATE)
        w.setsampwidth(SAMPLE_WIDTH)
        required_samples = DURATION * FRAMERATE
        data = array.array('h', [
            int(v) for v in audio_generator(required_samples, fetch_random_org_noise)
        ])
        w.writeframes(data)


if __name__ == '__main__':
    write_wav('./native_noise.wav', native_noise_generator)
    write_wav('./remote_noise.wav', remote_noise_generator)
