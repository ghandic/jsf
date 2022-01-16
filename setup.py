import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsf",
    version="0.3.2",
    author="ghandic",
    description="Creates fake JSON files from a JSON schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src", exclude=["tests"]),
    install_requires=["rstr", "faker", "smart_open", "jsonschema",
                      "typer", "pydantic", "python-dateutil", "text_unidecode"],
    url="https://github.com/ghandic/jsf",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "JSON Schema",
        "Fake data",
        "Test data",
        "Schema",
        "JSON",
        "Faker",
        "Hypothesis",
        "Rapid Prototype",
        "Data contract",
    ],
    zip_safe=True,
    python_requires=">=3.7",
    entry_points={"console_scripts": ["jsf=jsf.cli:app"]},
)
