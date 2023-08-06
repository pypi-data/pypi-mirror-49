import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="qrange",
    version="1.0.1",
    description="Working with ranges made simple",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Forfunckle/qrange",
    author="Forfunckle",
    author_email="cosminjames555@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)