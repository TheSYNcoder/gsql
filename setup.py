import setuptools


with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

__version__ = "1.0.0"

setuptools.setup(
    name="gsql",
    version=__version__,
    author="thesyncoder",
    author_email="sgd030@gmail.com",
    description="A Python application to interact with gsheets through SQL",
    long_description="A Python application to interact with gsheets through SQL",
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
