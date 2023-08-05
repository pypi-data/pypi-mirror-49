from distutils.core import setup

VERSION = '0.1.14'


with open('requirements.txt') as f:
    requires = f.read().splitlines()

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='wikiquote',
    packages=['wikiquote', 'wikiquote.langs'],
    version=VERSION,
    description='Retrieve quotes from any Wikiquote article.',
    long_description=long_description,
    author='Federico Tedin',
    author_email='federicotedin@gmail.com',
    install_requires=requires,
    url='https://github.com/federicotdn/wikiquote',
    download_url='https://github.com/federicotdn/wikiquote/archive/{}.tar.gz'.format(VERSION),
    keywords=['quotes', 'wikiquote', 'python', 'api', 'qotd', 'quote', 'day'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities'
    ]
)
