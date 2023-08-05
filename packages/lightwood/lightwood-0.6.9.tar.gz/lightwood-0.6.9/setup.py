import setuptools
from lightwood.version import lightwood_version
with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()
print(lightwood_version)
setuptools.setup(
    name="lightwood",
    version=lightwood_version,
    author="MindsDB Inc",
    author_email="jorge@mindsdb.com",
    description="MindsDB's goal is to make it very simple for developers to use the power of artificial neural networks in their projects. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mindsdb/mindsdb",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    python_requires=">=3.3"
)