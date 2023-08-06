# -*- coding: utf-8 -*-


"""monoshape setup module"""

from setuptools import setup

__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '1.1'
__maintainer__ = 'Borja González Seoane'
__email__ = 'dev@glezseoane.com'
__status__ = 'Production'


setup(
    name='monoshape',
    version='1.1',
    packages=['monoshape'],
    entry_points={
        'console_scripts': [
            'monoshape=monoshape.__main__:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=['filetype==1.0.5', 'pillow==6.1'],
    data_files=[('share/man/man1', ['manpages/monoshape.1']),
                ("", ["LICENSE"])],
    url='https://github.com/GlezSeoane/monoshape',
    download_url='https://github.com/GlezSeoane/monoshape/archive/v1.0.tar.gz',
    license='LICENSE',
    author='Borja González Seoane',
    author_email='dev@glezseoane.com',
    description='Extracts monochromatic shapes.',
    long_description='This program takes an image that has well '
                     'differentiated light and dark tones and extracts its '
                     'monochromatic shape in the desired colour with a '
                     'transparent background.',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
        'Topic :: Artistic Software',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Editors',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Software Development :: Libraries'
    ],
)
