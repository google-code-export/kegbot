#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

VERSION = "0.7.4"
SHORT_DESCRIPTION = "Kegbot kegerator controller software"
LONG_DESCRIPTION = """This package contains Kegbot core controller and Django
frontend package.

Kegbot is a hardware and software system to record and monitor access to a beer
kegerator.  For more information and documentation, see http://kegbot.org/

**Note:** This package is still *experimental* and subject to change.
"""

setup(
    name = "kegbot",
    version = VERSION,
    description = SHORT_DESCRIPTION,
    long_description = LONG_DESCRIPTION,
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
      'src/pykeg/bin/kegbot_twitter.py',
      'src/pykeg/bin/lcd_daemon.py',
      'src/pykeg/bin/rfid_daemon.py',
      'src/pykeg/bin/sound_server.py',
    ],
    install_requires = [
      'django >= 1.2',
      'django-imagekit >= 0.3.3',
      'django-registration',
      'django-socialregistration == 0.3.4',
      'django_extensions',
      #'MySQL-python',
      #'pil',
      'protobuf >= 2.3.0-1',
      'pylcdui >= 0.5.5',
      #'pysqlite>=2.0.3',
      'python-gflags >= 1.3',
      'South >= 0.7',
      'Sphinx',
      #'django_nose',
      'python-openid >= 2.2.5',  # removeme once PIL package works
      ### need pygooglechart
    ],
    dependency_links = [
        'http://dist.repoze.org/PIL-1.1.6.tar.gz',
        'http://kegbot.org/kmedia/protobuf-2.3.0-1.tgz',
        'http://kegbot.org/kmedia/python-openid-2.2.5.tgz',
    ],
    include_package_data = True,

)
