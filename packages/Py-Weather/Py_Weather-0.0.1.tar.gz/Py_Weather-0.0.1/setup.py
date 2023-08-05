from setuptools import setup
import setuptools

with open("README1.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Py_Weather',
    version='0.0.1',
    description='A weather information API',
    author= 'Kushal Bhavsar',
    # url = 'https://github.com/Spidy20/PyMusic_Player',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['weather','weather info'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['Py_Weather'],
    package_dir={'':'src'},
    install_requires = [
        'beautifulsoup4',
        'requests',
    ]
)
