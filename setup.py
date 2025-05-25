from setuptools import setup, find_packages
from pathlib import Path

# Read requirements.txt (for external dependencies)
def get_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="data_analysis",
    version="0.1",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=get_requirements(),
    python_requires=">=3.8",
)