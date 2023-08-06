import os.path
from setuptools import setup

# The directory containing this file
dir_ = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(dir_, "README.md")) as fid:
    README = fid.read()

setup(
    name='Filio',
    version='1.0.0',
    packages=['filio'],
    url='https://github.com/nerdloco/filio',
    license='MIT',
    long_description=README,
    author='nerdloco',
    long_description_content_type="text/markdown",
    author_email='gibsonruitiari@gmail.com',
    description='a cli python tool which checks for empty & broken files',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    install_requires=[
        "click", "asyncio"
    ],
    entry_points={"console_scripts": ["filio_=filio.__main__:main"]},

)
