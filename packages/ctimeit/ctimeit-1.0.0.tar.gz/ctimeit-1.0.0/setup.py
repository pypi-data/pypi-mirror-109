import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ctimeit",
    version="1.0.0",
    author="Vemund S. Schoyen",
    author_email="vemund@live.com",
    description="A python decorator for timing functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vemundss/ctimeit",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
