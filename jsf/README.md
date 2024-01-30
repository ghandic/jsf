<h1 align="center">
   <strong>jsf</strong><img src="docs/assets/imgs/index.png" width="50" style="position: absolute; padding-left:10px;">
</h1>

<p align="center">
    <a href="https://codecov.io/gh/ghandic/jsf" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/ghandic/jsf?color=%2334D058" alt="Coverage">
    </a>
    <a href="https://ghandic.github.io/jsf/index.html" target="_blank">
        <img src="https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat" alt="Docs">
    </a>
    <a href="https://pypi.org/project/jsf/" target="_blank">
        <img src="https://img.shields.io/pypi/v/jsf.svg" alt="PyPI Latest Release">
    </a>
    <br />
    <a href="https://github.com/ghandic/jsf/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
    </a>
    <a href="https://github.com/psf/black" target="_blank">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
    </a>
</p>

Use **jsf** along with fake data generators to provide consistent and meaningful fake data for your system.

## Main Features

- Provides out of the box data generation from any JSON schema 📦
- Extendable custom data providers using any lambda functions 🔗
- Multi level state for dependant data (eg multiple objects sharing value, such as children with same surname) 🤓
- Inbuilt validation of fake JSON produced ✅
- In memory conversion from JSON Schema to Pydantic Models with generated examples 🤯
- Seamless integration with [FastAPI](https://fastapi.tiangolo.com/) 🚀

## Installation

<div class="termy">

```console
$ pip install jsf

---> 100%
```

</div>

## Usage

### Basic 😊

```python
from jsf import JSF

faker = JSF(
    {
        "type": "object",
        "properties": {
            "name": {"type": "string", "$provider": "faker.name"},
            "email": {"type": "string", "$provider": "faker.email"},
        },
        "required": ["name", "email"],
    }
)

fake_json = faker.generate()
```

Results in ...

```python
{
    'name': 'Jesse Phillips', 
    'email': 'xroberson@hotmail.com'
}
```

### From JSON file 📁

```python
from jsf import JSF

faker = JSF.from_json("demo-schema.json")
fake_json = faker.generate()
```

<details markdown="1">
<summary>Or run straight from the <code>commandline</code>...</summary>

#### Native install

```bash
pip install jsf[cli]
jsf --schema jsf/tests/data/custom.json --instance wow.json
```

#### Docker

```bash
docker run -v $PWD:/data challisa/jsf jsf --schema /data/custom.json --instance /data/example.json
```

</details>

### FastAPI Integration 🚀

Create a file main.py with:

```python
from jsf import JSF
from fastapi import FastAPI

app = FastAPI(docs_url="/")
generator = JSF.from_json("custom.json")


@app.get("/generate", response_model=generator.pydantic())
def read_root():
    return generator.generate()

```

Run the server with:

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) and check out your endpoint. Notice the following are all automatically created:

- Schema with descriptions and examples
- Example response
- Data generation by clicking "try it out"

![Example Swagger UI - Page 1](docs/assets/imgs/ui-1.png)
![Example Swagger UI - Page 2](docs/assets/imgs/ui-2.png)
![Example Swagger UI - Page 3](docs/assets/imgs/ui-3.png)
![Example Swagger UI - Page 4](docs/assets/imgs/ui-4.png)

</div>

### Partially supported features

- string `contentMediaType` - only a subset of these are supported, however they can be expanded within [this file](jsf/schema_types/string_utils/content_type/__init__.py)  

## Credits

- This repository is a Python port of [json-schema-faker](https://github.com/json-schema-faker/json-schema-faker) with some minor differences in implementation.

## License

- [MIT License](/LICENSE)
