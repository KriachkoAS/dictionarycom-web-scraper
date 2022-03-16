from setuptools import setup

setup(
    name = 'dictionarycom-ipa-scraper',
    version = '2.1.0',
    description = 'ipa and complexity scraper of dictionary.com word page html',
    packages = ['scraper'],
    package_dir = {'': 'src'},
    install_requires = [
        'beautifulsoup4 >= 4.10.0, <5'
    ],
)

#pip install wheel
#python setup.py bdist_wheel sdist