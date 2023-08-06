# Helios

Monitors a stream and reports the audio levels

## Building

Installing from source is done as follows

    python3 setup.py install

### Development Install

When developing Helios, it is useful to use a virtual environment to
avoid poluting your desktop with unnecessary libraries. This is done using
[VirtualEnv](https://virtualenv.pypa.io/en/stable/).

Once VirtualEnv is installed, fork, clone the repo and create a virtual
environment:

    git clone https://salsa.debian.org/debconf-video-team/helios
    cd helios
    virtualenv -p python3 pyenv
    pyenv/bin/pip install -e .

Then the project can be edited and finally run as follows:

    pyenv/bin/helios <stream url>
