import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="open_1688",
    version="0.0.1",
    author="l3n641",
    author_email="hh250@qq.com",
    description="1688 api ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/l3n641/open_1688",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
