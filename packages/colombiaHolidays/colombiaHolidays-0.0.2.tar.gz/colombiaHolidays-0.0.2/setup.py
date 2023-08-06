import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colombiaHolidays",
    version="0.0.2",
    author="Oscar Cely",
    author_email="oscarcej@gmail.com",
    description="return the list of holidays existing on "
                "a determined year in Colombia",
    long_description="Based on [nequibc /colombia-holidays] "
                     "(https://github.com/nequibc/colombia-holidays) and "
                     "adapted to use as a python module to return "
                     "the list of holidays "
                     "existing on a determined year in Colombia",
    long_description_content_type="text/markdown",
    url="https://github.com/Oscarce10/colombiaHolidays",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)