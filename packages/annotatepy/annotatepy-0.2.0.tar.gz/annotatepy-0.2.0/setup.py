#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='annotatepy',
    version='0.2.0',
    description='Build git.sr.ht annotations for Python projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ivan Habunek',
    author_email='ivan@habunek.com',
    url='https://git.sr.ht/~ihabunek/annotatepy',
    project_urls={
        'Issue tracker': 'https://todo.sr.ht/ihabunek/annotatepy/',
    },
    keywords='sourcehut annotations python',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['annotatepy'],
    python_requires=">=3.6",
    install_requires=[
        "jedi",
    ],
    entry_points={
        'console_scripts': [
            'annotatepy=annotatepy.console:main',
        ],
    }
)
