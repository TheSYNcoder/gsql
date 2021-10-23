import setuptools
import versioneer

with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="gsql",
    version=versioneer.get_version(),
    author="thesyncoder",
    author_email="sgd030@gmail.com",
    description="A Python application to interact with gsheets through SQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
