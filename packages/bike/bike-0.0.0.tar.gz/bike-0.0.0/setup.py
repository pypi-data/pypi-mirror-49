import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="bike",
    version="0.0.0",
    description="A nice model",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    author="Manasses Lima",
    author_email="manasseslima@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["bike"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "realpython=bike.__main__:main",
        ]
    },
)