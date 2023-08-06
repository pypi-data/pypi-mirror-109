import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="altearnrpc",
    version="0.1.5",
    description="Un client Discord RPC pour Altearn",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Aeris1One/altearn-discord-rpc",
    author="Aeris One",
    author_email="aeris@e.email",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["altearnrpc"],
    include_package_data=True,
    install_requires=["pypresence", "tqdm"],
    entry_points={
        "console_scripts": [
            "altearnrpc=altearnrpc.__main__:main",
        ]
    },
)
