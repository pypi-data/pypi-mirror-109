"""myst-parser package setup."""
from importlib import import_module

from setuptools import find_packages, setup

setup(
    name="jupyter_federation",
    version=import_module("jupyter_federation.version").__version__,
    description=(
        "Jupyter Federation"
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/datalayer/jupyter-federation",
    project_urls={"Documentation": "https://jupyter-federation.readthedocs.io"},
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="datalayer",
    python_requires=">=3.6",
    install_requires=[
        "fastapi",
        "typing",
    ],
    extras_require={
        "sphinx": [],
        "code_style": [
            "flake8<3.8.0,>=3.7.0", 
            "black", 
            "pre-commit==1.17.0"
        ],
        "testing": [
            "coverage",
            "pytest>=3.6,<4",
            "pytest-cov",
            "pytest-regressions",
            "beautifulsoup4",
        ],
        "rtd": [
            "myst_parser",
            "pyyaml",
            "sphinx",
            "sphinxcontrib-bibtex",
            "ipython",
            "sphinx-book-theme",
            "sphinx_tabs"
        ],
    },
    zip_safe=True,
)
