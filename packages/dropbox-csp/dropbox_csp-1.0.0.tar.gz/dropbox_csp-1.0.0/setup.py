from setuptools import setup, find_packages


def extract_requirements(requirements_file):
	requirements = open(requirements_file, "r").read()
	listed_requirements = requirements.split("\n")[:-1]
	return listed_requirements


setup(
	name="dropbox_csp",
	author="Eddy Mwenda Mwiti",
	version="1.0.0",
	description="Dropbox wrapper client to upload data files toa folder",
	long_description=open("README.md", "r").read(),
	packages=find_packages(),
	include_package_data=True,
	install_requires=extract_requirements("requirements.txt"))
