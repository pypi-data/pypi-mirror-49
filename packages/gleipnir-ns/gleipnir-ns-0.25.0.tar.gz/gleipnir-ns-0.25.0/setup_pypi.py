import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gleipnir-ns",
    version="0.25.0",
    python_requires='>=3.6',
    install_requires=['numpy', 'scipy', 'pandas'],
    author="Blake A. Wilson",
    author_email="blakeaw1102@gmail.com",
    description="Python toolkit for Nested Sampling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoLab-VU/Gleipnir",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
