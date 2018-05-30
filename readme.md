# white noise generator


How to run this code:

```bash
$ git clone https://github.com/powersjcb/noisegenerator
$ cd noisegenerator
$ pipenv install
$ pipenv run py.test # ensure unit tests pass for your system

# creates remote_noise.wav and native_noise.wav in current directory
# native_noise.wav is created using python's random module
# remote_noise.wav is created using data from random.org
$ pipenv run python ./sound.py

```