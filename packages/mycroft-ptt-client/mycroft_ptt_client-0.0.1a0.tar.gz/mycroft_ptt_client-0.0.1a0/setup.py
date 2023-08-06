""" Install the mycroft_ptt_client package
"""
import os.path
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fd:
    long_description = fd.read()

setup(
    name='mycroft_ptt_client',
    version='0.0.1a',
    description='Mycroft Push-To-Talk Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AIIX/mycroft_ptt_client',
    keywords='mycroft ptt daemon client',
    packages=['mycroft_ptt_client'],
    install_requires=['python-libinput', 'mycroft-messagebus-client'],
    include_package_data=True,
    license='Apache',
    author='Aditya Mehra',
    author_email='aix.m@outlook.com',
    entry_points={
        'console_scripts': [
            'mycroft_ptt_client=mycroft_ptt_client.__main__:main',
            ]
        }
)
