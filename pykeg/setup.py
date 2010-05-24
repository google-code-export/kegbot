#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "kegbot",
    version = "0.7.0",
    description = "Kegbot keg controller software",
    author = "mike wakerly",
    author_email = "opensource@hoho.com",
    url = "http://kegbot.org/",
    packages = find_packages('src'),
    package_dir = {
      '' : 'src',
    },
    scripts = [
      'distribute_setup.py',
      'src/pykeg/bin/fb_publisher.py',
      'src/pykeg/bin/kegboard_daemon.py',
      'src/pykeg/bin/kegboard_monitor.py',
      'src/pykeg/bin/kegbot_admin.py',
      'src/pykeg/bin/kegbot_core.py',
      'src/pykeg/bin/kegbot_master.py',
      'src/pykeg/bin/lcd_daemon.py',
      'src/pykeg/bin/rfid_daemon.py',
      'src/pykeg/bin/sound_server.py',
    ],
    install_requires = [
      'django >= 1.0',
      'django-imagekit >= 0.3.3',
      'pylcdui >= 0.5.4',
      'python-gflags >= 1.3',
      'South >= 0.7',
      'MySQL-python',
      'django-registration',
      'pil',
      #'pysqlite>=2.0.3',
    ],
    include_package_data = True,

)
