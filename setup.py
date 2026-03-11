from setuptools import setup, find_packages

setup(
    name="cloudmatchpdf",
    version="0.1.0",
    author="Jose Jimenez",
    description="Motor de generación y compilación de LaTeX en la nube para Física y Data Science",
    packages=find_packages(),
    install_requires=[
        "requests",
        "sympy",
        "matplotlib",
        "numpy"
    ],
    python_requires=">=3.8",
)