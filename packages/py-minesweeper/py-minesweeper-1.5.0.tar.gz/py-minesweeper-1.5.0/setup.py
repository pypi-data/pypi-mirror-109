import os
from setuptools import setup

setup(
    name = "py-minesweeper",
    version = "1.5.0",
    author = "Tekcno",
    author_email = "tekcno@tekcno.com",
    description = ("Minesweeper engine for python"),
    packages=['pyminesweeper'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities"
    ],
)
