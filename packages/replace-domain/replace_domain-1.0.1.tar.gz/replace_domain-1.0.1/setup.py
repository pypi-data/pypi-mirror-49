import os
import re
from setuptools import setup, find_packages


def get_version(source):
    """
    Retrieve the version of a python distribution.

    version_file default is the <project_root>/_version.py

    :param source: Path to project root
    :return: Version string
    """
    version_str_lines = open(os.path.join(source, '_version.py'), "rt").read()
    version_str_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(version_str_regex, version_str_lines, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % os.path.join(source, os.path.basename(source)))


setup(
    name='replace_domain',
    version=get_version('replace_domain'),
    packages=find_packages(),
    install_requires=[
        'looptools',
    ],
    url='https://github.com/mrstephenneal/Dockerizer',
    entry_points={
        'console_scripts': [
            'replace_domain = replace_domain.replace_domain:main',
        ]
    },
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Nginx conf file string replacement.'
)
