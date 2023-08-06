import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycnet_devkit",
    version="0.0.2",
    author="spyc",
    author_email="unknown@gmail.com",
    description="A personal package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=['pandas','pandas-flavor'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)