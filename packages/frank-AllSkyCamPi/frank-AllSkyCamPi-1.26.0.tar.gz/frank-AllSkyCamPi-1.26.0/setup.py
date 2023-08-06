import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the allskycam file
#frankAllSkyCamPi = (HERE / "frank-AllSkyCamPi.md").read_text()
frankAllSkyCamPi="frank-AllSkyCamPi.md"

# This call to setup() does all the work
setup(
    name="frank-AllSkyCamPi",
    version="1.26.0",
    description="",
    long_description=frankAllSkyCamPi,
    long_description_content_type="text/markdown",
    url="https://github.com/sferlix/frank-AllSkyCamPi",
    author="Francesco Sferlazza",
    author_email="sferlazza@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["allskycam"],
    include_package_data=True,
    install_requires=["pytz"],
    entry_points={
        "console_scripts": [
            "allskycam=allskycam.__main__:main",
        ]
    },
)
