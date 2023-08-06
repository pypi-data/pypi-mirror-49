from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='loto',
    version='0.1.5',
    description='Decorator for tagging critical sections locking them out',
    long_description=long_description,
    description_content_type='text/markdown',
    long_description_content_type='text/markdown; charset=UTF-8; variant=GFM', 
    url='https://github.com/mardigontoler/loto',
    author='Mardigon Toler',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),  # Required
    python_requires='>=3',
    install_requires=['pytest'],
)
