from setuptools import setup
import re
from os.path import join, dirname


def readme():
    with open('readme.md', encoding='utf-8') as f:
        return f.read()


VERSION = "1.0.8"


setup(
    packages=['SSML'],
    name='SSML',
    author="Shinyhero36",
    url="https://github.com/Shinyhero36/SSML",
    description="This is a description",
    long_description=readme(),
    long_description_content_type='text/markdown',
    version=VERSION,
    license="GNU General Public License v3.0",
    project_urls={
        'Source': 'https://github.com/Shinyhero36/SSML/',
        'Tracker': 'https://github.com/Shinyhero36/SSML/issues',
    },
    python_requires='>=3.6',
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Topic :: Home Automation"
    ],
    keywords='ssml python google alexa assistant',
)
