import setuptools
with open(r'D:\Репозиторий\myrepository1\csv_file\Readme.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='csv_file',
	version='1.0',
	author='Bernax27',
	author_email='Roman-16016@yandex.ru',
	description='This repository which was created to facilitate working with csv',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Bernax27/myrepository1/tree/main',
	packages=['csv_project'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)