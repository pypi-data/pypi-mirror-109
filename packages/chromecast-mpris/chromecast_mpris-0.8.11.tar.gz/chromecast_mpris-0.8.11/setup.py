__author__ = 'Alex DeLorenzo'
from typing import Dict, List
from setuptools import setup
from pathlib import Path


NAME: str = 'chromecast_mpris'
VERSION: str = '0.8.11'
LICENSE: str = 'AGPL-3.0'
PY_VERSION: str = '>=3.6'


ENTRY_POINTS: Dict[str, List[str]] = {
  'console_scripts': [
    f'{NAME} = {NAME}.command:cmd',
  ]
}

REQS: List[str] = Path('requirements.txt') \
  .read_text() \
  .split('\n')

README: str = Path('README.md').read_text()

ASSET_DIRS: List[str] = [
  'assets/chromecast_mpris.desktop',
  'assets/icon/cc-*.png'
]

PKG_DATA: Dict[str, List[str]] = {
  NAME: ASSET_DIRS
}


setup(
  name=NAME,
  version=VERSION,
  description='📺 Control Chromecasts from Linux and D-Bus',
  long_description=README,
  long_description_content_type='text/markdown',
  url='https://github.com/alexdelorenzo/chromecast_mpris',
  author=__author__,
  license=LICENSE,
  packages=[NAME],
  zip_safe=True,
  install_requires=REQS,
  entry_points=ENTRY_POINTS,
  python_requires=PY_VERSION,
  package_data=PKG_DATA,
)
