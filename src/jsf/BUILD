python_sources(name="src")

python_requirements(name="reqs")

python_distribution(
    name="jsf-dist",
    entry_points={
        "console_scripts": {
            "jsf": "jsf.cli:app"
        },
    },
    dependencies=[":src"],
    provides=python_artifact(
        name="jsf",
        version="0.5.1",
        author="ghandic",
        description="Creates fake JSON files from a JSON schema",
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
    ),
)

    
    
    
    
    