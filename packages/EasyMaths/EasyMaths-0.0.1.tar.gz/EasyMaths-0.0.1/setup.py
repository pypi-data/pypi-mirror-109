
from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'To make Maths Easier in Python.'
LONG_DESCRIPTION = 'This package is made only for pure beginners.'

# Setting up
setup(
    name="EasyMaths",
    version=VERSION,
    author="The Vast (Youtuber)",
    author_email="ggrakesh3355@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)