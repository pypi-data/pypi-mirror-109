from setuptools import setup, find_packages
import os

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

long_description = open('README.md', 'r').read() + '\n\n' + open(os.path.join(os.getcwd(),'CHANGELOG.md'), 'r').read()

setup(
    name='progressbar_easy',
    version='1.0.4.3',
    description='A simple progressbar to track progress with built in-timer that estimates remaining time',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Braxton Brown',
    author_email='braxton.brown@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='progressbar, progress bar, progressbar_easy, easy progressbar, easy progress bar',
    packages=find_packages(),
    install_requires=['']
)