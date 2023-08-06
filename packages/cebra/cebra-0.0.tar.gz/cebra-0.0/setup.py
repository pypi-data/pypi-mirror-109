import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cebra",
    version="0.0",
    author_email="steffen@bethgelab.org",
    description="CEBRA",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)