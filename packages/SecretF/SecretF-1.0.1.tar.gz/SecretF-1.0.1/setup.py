import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SecretF",
    version="1.0.1",
    author="Fedorenko Timur",
    author_email="tim.fedorenko@mail.ru",
    description="Secret File",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HardHook/SecretF",
    classifiers=[
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.9",
    ],
    package_dir={"": "scr"},
    packages=setuptools.find_packages(where="scr"),
)