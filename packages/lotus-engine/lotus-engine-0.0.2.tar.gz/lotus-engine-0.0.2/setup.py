from setuptools import setup
from os import path

DIR = path.dirname(path.abspath(__file__))
INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

setup(
    name='lotus-engine',
    packages=['lotus_engine'],
    description="A android reverse tool",
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_PACKAGES,
    version='0.0.2',
    url='http://github.com/vforkliu/lotus',
    author='forkliu',
    author_email='vforkliu@gmail.com',
    keywords=['android', 'unicorn', 'emulator'],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-sugar'
    ],
    package_data={
        # include json and pkl files
        '': ['*.json', 'models/*.pkl', 'models/*.json'],
    },
    include_package_data=True,
    python_requires='>=3'
)