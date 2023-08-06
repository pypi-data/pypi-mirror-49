import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyimprove",
    version="0.0.1",
    author="William Young",
    author_email="william.w.c.young@hotmail.com",
    description="Automated Program Repair of Python Source-Code Using Genetic Improvement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/WilliamWCYoung/pyimprove",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
