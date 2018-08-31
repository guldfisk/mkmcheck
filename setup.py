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
	dependency_links=[
		'https://github.com/guldfisk/orp/tarball/master#egg=orp-1.0',
		'https://github.com/guldfisk/mtgorp/tarball/master#egg=mtgorp-1.0',
	],
	install_requires=[
		'orp',
		'mtgorp',
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
	]
)