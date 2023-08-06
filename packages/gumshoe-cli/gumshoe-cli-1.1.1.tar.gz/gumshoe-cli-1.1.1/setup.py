"""Setup for Habito app."""

from setuptools import setup, find_packages


setup(
    name="gumshoe-cli",
    version="1.1.1",
    description="Your habit tracking command line tool.",
    long_description="Your habit tracking command line tool.",
    url="",
    author="Philip Csaplar",
    author_email="philip@osit.co.za",

    packages=find_packages(exclude=["documentation", "tests*"]),
    entry_points={
        "console_scripts": ["gumshoe=gumshoe.main:cli"],
    },
    install_requires=["setuptools", "click", "terminaltables"],

    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    keywords="habits goals track tracking quantified self",
)
