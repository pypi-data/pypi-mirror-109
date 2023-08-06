import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
	'Operating System :: OS Independent',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]

setuptools.setup(
	name='stark-utilities',
	version='0.0.1',
	description='Stark utilities',
	long_description=long_description,
    long_description_content_type="text/markdown",
	url='',
	author='Stark Digital Media Services Pvt. Ltd.',
	author_email='starkengg81@gmail.com',
	License='MIT',
	classifiers=classifiers,
	keywords=["stark", "utilities", "stark-utilities"],
	python_requires='>=3.6',
	packages=setuptools.find_packages(),
	install_requires=[
	'requests',
	'cryptography==3.3.1',
	'oauthlib',
	'shortuuid',
	]
)
