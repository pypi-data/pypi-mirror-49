import setuptools
import io
import os
import sys

required = ['redis']

here = os.path.abspath(os.path.dirname(__file__))

with open("readconfig/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="readconfig",
    version="0.0.6",
    author="Jason Duncan",
    author_email="jason.matthew.duncan@gmail.com",
    description="Read redis DB config for other modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jduncan8142/read_config",
    install_requires=required,
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_data={'readconfig': ['requirements.txt', 'README.md', 'LICENSE']},
    py_modules=[
        'readconfig.py'
    ],
)
