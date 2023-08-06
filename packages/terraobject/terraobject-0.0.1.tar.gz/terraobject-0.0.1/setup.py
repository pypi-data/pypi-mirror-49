import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terraobject",
    version="0.0.1",
    author="Joao Gilberto Magalhaes",
    author_email="joao@byjg.com.br",
    description="Common Terraobject package",
    long_description="Common Terraobject package",
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/byjg/terraobject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)