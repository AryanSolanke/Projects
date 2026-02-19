from setuptools import setup, find_packages

setup(
    name="aryan-advanced-calculator",
    version="1.2.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "calculator=calculator.main:main",
        ],
    },
    python_requires=">=3.10",
    author="Aryan Solanke",
    description="Advanced modular calculator",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
