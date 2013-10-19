#!/usr/bin/env python

from distutils.core import setup

setup(name = 'MoodPy',
      version = '0.1',
      description = 'Python Interface for MoodlightUSB',
      long_description = open('README.txt').read(),
      author = 'Julius Roob',
      author_email = 'julius@juliusroob.de',
      url = 'https://github.com/Zottel/MoodPy',
      packages = ['moodlight'],
      scripts = [''],
      license = 'MIT License',
      requires = ["pyusb (>=1.0.0)"],
     )
