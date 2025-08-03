from setuptools import setup, find_packages

setup(
    name="pyconfigloader",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PyYAML>=6.0.2"
    ],
    author="Etienne Galecki",
    description="Application configuration loader",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires=">=3.11",
)