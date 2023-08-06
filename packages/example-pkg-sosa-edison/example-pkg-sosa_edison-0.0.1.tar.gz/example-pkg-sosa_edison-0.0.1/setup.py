import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-sosa_edison",
    version="0.0.1",
    author="Sosa Edison",
    author_email="sosa_edison@hotmail.com",
    description="A small example package",
    long_description="some stuff",
    long_description_content_type="text/markdown",
    url="https://github.com/sosaedison/Flask_Tracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
