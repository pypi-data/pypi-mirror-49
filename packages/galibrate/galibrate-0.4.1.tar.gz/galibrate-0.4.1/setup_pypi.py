import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="galibrate",
    version="0.4.1",
    python_requires='>=3.6',
    install_requires=['numpy', 'scipy'],
    author="Blake A. Wilson",
    author_email="blakeaw1102@gmail.com",
    description="Python toolkit for continuous Genetic Algorithm optimization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blakeaw/GAlibrate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
