python_sources(name="src")

resources(
    name="build_resources",
    sources=["README.md", "LICENSE"],
)

python_distribution(
    name="jsf-dist",
    entry_points={
        "console_scripts": {"jsf": "jsf.cli:app"},
    },
    dependencies=[
        ":src",
        ":build_resources",
        "./tests:tests",
    ],
    long_description_path="README.md",
    provides=python_artifact(
        name="jsf",
        version="0.11.1",
        author="ghandic",
        description="Creates fake JSON files from a JSON schema",
        url="https://github.com/ghandic/jsf",
        long_description_content_type="text/markdown",
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
        python_requires=">=3.8",
        extras_require={"cli": ["typer>=0.7.0"]},
    ),
)
