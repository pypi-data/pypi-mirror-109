from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Mixshift analysis'
LONG_DESCRIPTION = 'A package that helps in understanding the changes in the metrics over the period/between the groups using mixshift analysis'

# Setting up
setup(
    name="mixshift",
    version=VERSION,
    author="Vinoth Loganathan",
    author_email="<vinothloganathan@outlook.com>",
    description=DESCRIPTION,
    long_description= LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    py_modules=["mixshift"],             # Name of the python package
    package_dir={'':'mixshift/src'},     # Directory of the source code of the package
    keywords=['python', 'mixshift', 'KPI', 'month', 'mom', 'yoy','wow'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
