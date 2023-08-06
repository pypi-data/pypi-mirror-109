import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
	'Operating System :: OS Independent',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]

setuptools.setup(
	name='stark-rest-apiresponse',
	version='0.0.3',
	description='Easy way to get the standard rest api response',
	long_description=long_description,
    long_description_content_type="text/markdown",
	url='',
	author='Stark Digital Media Services Pvt. Ltd.',
	author_email='starkengg81@gmail.com',
	License='MIT',
	classifiers=classifiers,
	keywords=["stark", "rest-api", "rest-api-response", "stark-rest-apiresponse"],
	python_requires='>=3.6',
	packages=setuptools.find_packages(),
)
