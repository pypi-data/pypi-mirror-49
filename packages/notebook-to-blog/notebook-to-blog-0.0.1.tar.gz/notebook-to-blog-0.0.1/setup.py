from pathlib import Path
from setuptools import setup, find_packages


DIR = Path(__file__).parent

setup(
    name="notebook-to-blog",
    version="0.0.1",
    description="Convert a Jupyter notebook to blog ready format",
    long_description=(DIR / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Chris Rinaldi",
    license="MIT",
    author_email="cgrinaldi@gmail.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=["Click", "PyGithub", "python-dotenv"],
    entry_points={"console_scripts": ["notebook_to_blog = notebook_to_blog.cli:main"]},
)
