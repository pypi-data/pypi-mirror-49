import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_sql_generator",
    version="0.9.7",
    author="Tim Muzzin",
    author_email="timmuzzin@gmail.com",
    description="Simple Package for generating SQL from Dictionary Objects.",
    long_description="Simple Package for generating SQL from Dictionary \
        Objects. Helpful when dealing with large tables with lots of fields.",
    long_description_content_type="text/markdown",
    url="https://github.com/tmuzzin/PythonSQLGenerator",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)