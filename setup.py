from setuptools import setup, find_packages

setup(
    name="archiforge",
    version="0.4.2",
    packages=find_packages(),
    install_requires=[
        "click",
        "google-genai",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "archiforge=archiforge.cli:cli",
        ],
    },
)