import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amqpcli",
    version="0.0.1",
    author="Martin Hong",
    author_email="hongzeqin@gmail.com",
    description="a Python interactive shell to act as an AMQP client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Martin91/amqpcli",
    packages=setuptools.find_packages(),
    scripts=['bin/amqpcli'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Communications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)