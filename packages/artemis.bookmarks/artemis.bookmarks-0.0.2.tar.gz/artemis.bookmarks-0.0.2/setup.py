from setuptools import setup, find_packages


def file(name: str) -> str:
	with open(name, 'r') as f:
		return f.read()


setup(
	name='artemis.bookmarks',
	version='0.0.2',
	description='a small bookmark api',
	long_description=file('README.md'),
	long_description_content_type='text/markdown',
	url='https://git.artemix.space/?p=bookmarks;a=summary',
	license='CNPLv6',
	author='root',
	author_email='pypi@artemix.org',
	packages=find_packages(),
	package_data={'': [
		'bookmarks/templates/*',
		'bookmarks/assets/*',
	]},
	include_package_data=True,
	install_requires=[
		'python-slugify',
		'Flask',
		'flask_sqlalchemy',
		'toml',
	],
	classifiers=[
		'Environment :: Console',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Internet',
		'Typing :: Typed',
	]
)
