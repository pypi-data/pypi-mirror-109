from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Quiffen'
LONG_DESCRIPTION = 'A Python package for parsing Quicken Interchange Format (QIF) files.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="quiffen",
    version=VERSION,
    author="Isaac Harris-Holt",
    author_email="isaac@harris-holt.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'qif'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)