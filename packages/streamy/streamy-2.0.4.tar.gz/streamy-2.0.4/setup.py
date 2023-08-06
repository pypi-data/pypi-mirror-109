from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os, sys


# From here: http://pytest.org/2.2.4/goodpractises.html
class RunTests(TestCommand):
    DIRECTORY = 'test'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [self.DIRECTORY]
        self.test_suite = True

    def run_tests(self):
        # Import here, because outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        if errno:
            raise SystemExit(errno)


def _version():
    with open('streamy.py') as fp:
        line = next(i for i in fp if i.startswith('__version__'))
        return line.strip().split()[-1].strip("'")


NAME = 'streamy'
OWNER = 'timedata-org'
VERSION = _version()

URL = 'http://github.com/{OWNER}/{NAME}'.format(**locals())
DOWNLOAD_URL = '{URL}/archive/{VERSION}.tar.gz'.format(**locals())


if __name__ == '__main__':
    setup(
        name='streamy',
        version=_version(),
        description=('streamy splits a stream into a stream of strings that are'
                     ' complete JSON expressions'),
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url=URL,
        download_url=DOWNLOAD_URL,
        license='MIT',
        packages=find_packages(exclude=['test']),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        tests_require=[],
        cmdclass={'test': RunTests},
        keywords=['git', 'import'],
        include_package_data=True,
        install_requires=[],
    )
