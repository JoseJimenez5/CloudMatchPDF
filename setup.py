from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="symtex",
    version="0.1.2",
    author="Jose Jimenez",
    author_email="jose.jimenez05@epn.edu.ec", 
    description="Framework de generación de reportes LaTeX científicos vía Cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoseJimenez5/CloudMatchPDF", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    install_requires=[
        "requests>=2.31.0",
        "sympy>=1.12",
        "numpy>=1.26.4",
        "matplotlib>=3.8.0"
    ],
    extras_require={
        "dev": ["pytest>=8.0.2", "black", "flake8"],
    },
    python_requires=">=3.8",
    include_package_data=True,
)
