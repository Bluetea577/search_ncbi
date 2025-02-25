from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="search_ncbi",
    version="0.1.2",
    author="Li Mingyang",
    author_email="limingyang577@163.com",
    description="A package for searching and processing NCBI data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bluetea577/search_ncbi",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "biopython>=1.78",
        "pandas>=1.3.0",
        "tqdm>=4.46.0",
        "xmltodict",
        "requests",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "black>=21.9b0",
            "flake8>=3.9.2",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "searchncbi=search_ncbi.cli:main",
        ],
    },
)