import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deadman_state_machine",
    version="0.1.0",
    author="Roger Sicart",
    author_email="roger.sicart@gmail.com",
    description="Deadman State Machine package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rsicart/deadman-state-machine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
)
