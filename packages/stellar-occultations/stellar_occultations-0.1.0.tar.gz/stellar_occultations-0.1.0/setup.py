import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="stellar_occultations",
    version="0.1.0",
    description="Tools to calculate diffraction patterns by stellar occultations",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ferwazz/stellar_occultations",
    aauthor="Joel H. Castro-Chacón & Alvarez-Santana. F.I",
    author_email="joelhcch@astro.unam.mx ",
    license="GNU AFFERO GENERAL PUBLIC LICENSE",
    packages=["stellar_occultations"],
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
    ],
    python_requires=">=3.6",
)