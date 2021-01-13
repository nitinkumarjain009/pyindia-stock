
from setuptools import setup, Extension
from setuptools import find_packages

with open("README.md") as f:
    long_desc = f.read()

if __name__ == "__main__":
    setup(
        name="pyindia_stock",
        scripts=['scripts/pyindia_stock', ],
        version="0.0.1",
        description="Stock Prediction using FBProphet",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        author="Shivanand",
        author_email="shivanandnaduvin@gmail.com",
        url="https://github.com/Shivananmn/pyindia-stock",
        license="MIT License",
        packages=find_packages(),
        include_package_data=True,
        install_requires=["fbprophet>=0.7.1", ],
        python_requires=">3.5.2",
    )
