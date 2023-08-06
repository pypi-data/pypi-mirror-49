import setuptools


setuptools.setup(
		name='bitcoinlantern',
		description='A bitcoin and lightning library that focuses on wallets and rpc.',
		long_description= 'A small Bitcoin library that\'s delightfully easy to read and easy to use.',
		author='Leon Johnson',
		author_email='leon.johnson@me.com',
		version='0.1',
		packages=setuptools.find_packages(),
		classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		],
		python_requires='>=3',
	)