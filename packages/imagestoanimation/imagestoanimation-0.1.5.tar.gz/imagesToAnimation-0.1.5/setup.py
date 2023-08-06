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
    'version': '0.1.5',
    'description': 'Converts a series of images to an animation using OpenCV',
    'long_description': 'Convert a folder of images to an animation\n\nIf using PowerPoint 2016 you can save all slides as images to be used as input\n\nUse settings.conf or command line arguments to configure the input/output/etc\n\nInstall with \n`pip install imagestoanimation` \n\n\nUsage:\n\n```\nimgvid [-h] [-s SETTINGS] [-d DIRECTORY] [-f FILEFORMAT] [-c CODEC]\n              [-o OUTPUT] [-r RATE] [-W WIDTH] [-H HEIGHT]\n\nArgs that start with \'--\' (eg. -d) can also be set in a config file (*.conf or\nspecified via -s). Config file syntax allows: key=value, flag=true,\nstuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). If an arg is\nspecified in more than one place, then commandline values override config file\nvalues which override defaults.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s SETTINGS, --settings SETTINGS\n                        Config file path, usually *.conf\n  -d DIRECTORY, --directory DIRECTORY\n                        Directory containing frame files\n  -f FILEFORMAT, --fileformat FILEFORMAT\n                        Naming convention for frame files\n  -c CODEC, --codec CODEC\n                        Codec as FOURCC, see http://www.fourcc.org/codecs.php\n  -o OUTPUT, --output OUTPUT\n                        Output file name\n  -r RATE, --rate RATE  Frames Per Second\n  -W WIDTH, --width WIDTH\n                        Output frame width\n  -H HEIGHT, --height HEIGHT\n                        Output frame height\n\n```\n\nExample:\n```\nimgvid -d="input" -f=Slide[0-9]*.PNG -c=XVID -o=output.avi -r=15 -w=1280 -h=720\n```\n\n',
    'author': 'jpsmithnl',
    'author_email': 'jp.smith@mun.ca',
    'url': 'https://github.com/jpsmithnl/imagesToAnimation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
