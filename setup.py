#!/usr/bin/env python3

"""
Author: Benedikt Vollmerhaus
License: MIT
"""

from pathlib import Path

from setuptools import setup


def get_version() -> str:
    """
    Return the BlurWal version from the version module.

    :return: The BlurWal version
    """
    base_dir = Path(__file__).parent
    version_file = base_dir / 'blurwal/_version.py'

    version = {}
    exec(version_file.read_text(), version)
    return version['__version__']


VERSION = get_version()

#: The project repository
PROJECT_URL = 'https://gitlab.com/BVollmerhaus/blurwal'
#: The current release archive
RELEASE_URL = f'{PROJECT_URL}/-/archive/{VERSION}/blurwal-{VERSION}.tar.gz'

setup(
    name='BlurWal',
    version=VERSION,
    description='Smoothly blurs the wallpaper when windows are opened.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    keywords=['blur', 'wallpaper', 'desktop', 'ricing'],
    license='MIT',

    author='Benedikt Vollmerhaus',
    author_email='pypi@vollmerhaus.org',
    url=PROJECT_URL,
    download_url=RELEASE_URL,

    packages=['blurwal'],
    entry_points={'console_scripts': ['blurwal=blurwal.__main__:main']},

    python_requires='>=3.6',
    install_requires=['python-xlib', 'ewmh'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-mock', 'pytest-datadir'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment'
    ],
)
