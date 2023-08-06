from setuptools import setup, find_packages


requirements_file = open("requirements.txt")
# Remove newline characters in the list of requirements
requirements = [requirement.strip() for requirement in \
				requirements_file.readlines()]

setup(
	name="res_access_crypto",
	version="1.0.0",
	description="A python module with encryption and decryption\
				algorithms for RSA based IBE and AES",
	packages=find_packages(),
	include_package_data=True,
	long_description=open("README.md", "r").read(),
	install_requires=requirements,
	author="Eddy Mwenda Mwiti"
)
