import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdbg-bcit",
    version="1.0." + input("Version: "),
    author="",
    author_email="",
    description="A Python debugger for learner which print out all changes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y5bcit/pdbg.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)