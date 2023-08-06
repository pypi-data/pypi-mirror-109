from setuptools import setup, find_packages

with open("README.md", "r") as f:
	long_description = f.read()

setup(name="bloxlink",
	version="0.0.1",
	description="Package for Bloxlink",
	url="https://github.com/bloxlink/roblox",
	keywords=["async", "roblox", "bloxlink"],
	author="tigerism",
	author_email="admin@blox.link",
	license="MIT",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Operating System :: OS Independent"
	],
	long_description=long_description,
	long_description_content_type="text/markdown",
	zip_safe=False
)
