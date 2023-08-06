import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="decorata",
    version="0.0.1-alpha.1",
    author="jinoan",
    author_email="jinoan89@gmail.com",
    description="Convenient dataset maker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jinoan/decorata.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)