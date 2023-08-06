from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sensorbucket',
    version='0.1.3',
    author='Tim van Osch',
    author_email='timvosch@pollex.nl',
    packages=['sensorbucket'],
    url='http://pypi.python.org/pypi/Sensorbucket/',
    license='LICENSE',
    description='Provides interaction with the Sensorbucket API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "dataclasses-json"
    ]
)
