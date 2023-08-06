import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvizwizards",
    version="0.0.4",
    author="Sathwik Vangari",
    author_email="sathwik.mohan@gmail.com",
    description="A small visualization package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)