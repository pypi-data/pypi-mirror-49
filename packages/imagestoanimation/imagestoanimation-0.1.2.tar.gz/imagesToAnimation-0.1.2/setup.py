# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['imagestoanimation']

package_data = \
{'': ['*']}

install_requires = \
['configargparse>=0.14.0,<0.15.0', 'opencv-python>=4.1,<5.0']

entry_points = \
{'console_scripts': ['imgvid = imagesToAnimation:run']}

setup_kwargs = {
    'name': 'imagestoanimation',
    'version': '0.1.2',
    'description': 'Converts a series of images to an animation using OpenCV',
    'long_description': None,
    'author': 'jpsmithnl',
    'author_email': 'jp.smith@mun.ca',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
