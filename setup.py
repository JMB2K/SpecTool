from distutils.core import setup
import py2exe, os

setup(
	windows=['./spectool.py'],
	name='SpecTool',
	version='0.1',
	packages=['appJar', 'PyPDF2', 'collections'],
	url='',
	license='',
	author='JB',
	author_email='jonathanmb2000@outlook.com',
	description='Tool for renaming files and building specs',
	options={'py2exe': {'packages': ['appJar', 'PyPDF2']}}

	
    )
