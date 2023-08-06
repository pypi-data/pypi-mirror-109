
from setuptools import setup

setup(
    name='pyvidnteract',
    version='0.1.0',
    description='A way to interact with video files in python.',
    long_description='I am writing docs currently.\nCombine frames without ffmpeg!',
    install_requires=["Pillow", "python-opencv"],
    packages=["VidInteract"]
    )

