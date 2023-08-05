#!/usr/bin/env python
import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'dsocli'
DESCRIPTION = 'DevSecOps CLI'
REQUIRES_PYTHON = '>=3.9.0'
URL = "https://github.com/ramtinkazemi/devsecops"
EMAIL = 'ramtin.kazemi@gmail.com'
AUTHOR = 'Ramtin Kazemi'

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------


here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


with open(os.path.join(here, 'src', NAME, 'version.py')) as f:
    exec(f.read(), globals())

releaseCounter = os.getenv('DSO_RELEASE_NUMBER') or 0

version = f"{__version__}.{releaseCounter}"

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    project_urls={
        'Documentation': URL,
        'Source': URL
    },
    packages=find_packages('src', exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir = { '' : 'src/' }, 
    entry_points={
        'console_scripts': [f'dso={NAME}.cli:cli'],
    },
    install_requires=open(os.path.join(here, 'requirements/prod.in'), 'r').readlines(),
    extras_require=None,
    include_package_data=True,
    license='GPLV3',
    license_files = 'LICENSE.md',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    # cmdclass={
    #     'upload': UploadCommand,
    # },
)
