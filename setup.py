from io import open

from setuptools import find_packages, setup

with open('eyapm/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.1.0'

REQUIRES = ['click>=7.0', 'tqdm>=4.29']

setup(
    name='eyapm',
    version=version,
    description='',
    long_description='',
    author='riag',
    author_email='riag@163.com',
    maintainer='riag',
    maintainer_email='riag@163.com',
    url='https://github.com/riag/eyapm',
    license='Apache-2.0',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(exclude='test*'),
    entry_point={
        'console_scripts': [
            'eyapm=eyapm.cli:main'
        ]
    }
)
