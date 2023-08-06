import setuptools
with open(r'C:\Users\Computer\Desktop\CopyFilesHind\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='CopyFilesHind',
	version='1.0.0',
	author='Hindarsfjall',
	author_email='shubenkov@tuta.io',
	description='With this code, you can copy all the files from your repository and find the largest of copied files.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['CopyFilesHind'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)