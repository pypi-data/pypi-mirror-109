import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
#README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Krish",
    version="1.0.4",
    description="Meet A new A.I. - Krish",
    long_description_content_type="text/markdown",
    author="Mausam Kaushal",
    author_email="tbot1738@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["v1"],
    include_package_data=True,
    install_requires=["pyttsx3","speechrecognition","wikipedia",
    "youtube-search-python","pafy"],
    entry_points={
        "console_scripts": [
            "Krish=v1.__main__:main",
        ]
    },
)