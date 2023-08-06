import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "youngtest",
    version = "1.1",
    author = "Lue Young",
    author_email = "lueyoung7@gmail.com",
    description = "this is for test",
    long_description = "long_description",
    long_description_content_type = "text/markdown",
    url = "https://github.com/humstarman/young_test_package",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
