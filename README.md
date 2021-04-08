# jsf

<img src="docs/assets/imgs/index.png" width="100" >

[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://ghandic.github.io/jsf/index.html)
[![PyPI Latest Release](https://img.shields.io/pypi/v/jsf.svg)](https://pypi.org/project/jsf/)
[![License](https://img.shields.io/pypi/l/jsf.svg)](https://github.com/ghandic/jsf/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is it

This repository is a Python port of [json-schema-faker](https://github.com/json-schema-faker/json-schema-faker) with some minor differences in implementation.

> Use **jsf** along with fake generators to provide consistent and meaningful fake data for your system.

## Main Features

* Provides out of the box data generation from any JSON schema
* Extendable custom data providers using any lambda functions
* Multi level state for dependant data (eg multiple objects sharing value, such as children with same surname)
* Inbuilt validation of fake JSON produced

## Where to get it

The source code is currently hosted on GitHub at: https://github.com/ghandic/jsf

Binary installers for the latest released version are available at the [Python package index](https://pypi.org/project/jsf/)

```bash
pip install jsf
```

## Dependencies

* faker - For fake data provisioning
* rstr - For building strings from regex patterns
* smart_open - For opening external $ref
* jsonschema - For schema/instance validation
* typer - For neat commandline applications
* dataclasses_json - For easy dataclass serialization

## License

* [MIT License](/LICENSE)

## Usage

### As a program

* pip install jsf
* In your code where you need to you will be using jsf you can refer to below script as reference:

```python
from jsf import JSF

faker = JSF.from_json("demo-schema.json")
fake_json = faker.generate()
```

### From the commandline

#### Raw install

```bash
jsf --schema src/tests/data/custom.json --instance wow.json
```

#### Docker

```bash
docker build . -t challisa/jsf
docker run -v $PWD:/data challisa/jsf jsf --schema /data/src/tests/data/custom.json --instance /data/wow.json
```

## Contributing to jsf

To contribute to jsf, follow these steps:

1. Fork the repository
2. Create a branch in your own fork: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request back to our fork.
