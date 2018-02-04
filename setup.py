from setuptools import setup,find_packages

setup(
    name="gob",
    author="David Kleiven",
    version=1.0,
    packages=find_packages(),
    package_data={"gob":["data/*"]}
)
