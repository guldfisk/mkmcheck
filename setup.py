from setuptools import setup
import os

def package_files(directory):
    paths = []
    for path, directories, file_names in os.walk(directory):
        for filename in file_names:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('mkmcheck')

setup(
    name='mkmcheck',
    version='1.0',
    packages=['mkmcheck'],
    package_data={'': extra_files},
    install_requires=[
        'orp @ https://github.com/guldfisk/orp/tarball/master#egg=orp-1.0',
        'mtgorp @ https://github.com/guldfisk/mtgorp/tarball/master#egg=mtgorp-1.0',
        'secretresources @ https://github.com/guldfisk/secretresources/tarball/master#egg=secretresources-1.0',
        'lazy-property',
        'multiset',
        'appdirs',
        'frozendict',
        'requests',
        'apiclient',
        'oauth2client',
        'httplib2',
        'numpy',
        'promise',
        'sqlalchemy',
        'marshmallow',
        'marshmallow_sqlalchemy',
        'marshmallow_enum',
        'marshmallow_oneofschema @ https://github.com/guldfisk/marshmallow_oneofschema/tarball/master#egg=marshmallow_oneofschema-1.0',
    ]
)
