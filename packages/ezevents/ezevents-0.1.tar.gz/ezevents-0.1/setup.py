from setuptools import setup
from os import path

DIR = path.dirname(path.abspath(__file__))
INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

setup(
    name='ezevents',
    packages=['ezevents'],
    description="View your upcoming events and add events to your Google Calendar",
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_PACKAGES,
    include_package_data=True,
    version='0.1',
    url='http://github.com/CyberDrudge/EZEvents',
    author='Satyam Saxena',
    author_email='cyberdrudge77@gmail.com',
    keywords=['calendar', 'python', 'events'],
    python_requires='>=2.6'
)