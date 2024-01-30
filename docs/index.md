---
hide:
  - navigation
---

# Getting Started

## Installation

<!-- termynal -->
```bash
$ pip install jsf
---> 100%
Installed
```

## Usage

### From your Python program

```python
from jsf import JSF

faker = JSF.from_json("demo-schema.json")
fake_json = faker.generate()
```

### From the command line

#### System installation

First, you'll need to install `jsf[cli]` as it has the additional dependencies for the command line tools.

<!-- termynal -->
```bash
$ pip install jsf[cli]
---> 100%
Installed
```

Now the cli is installed, all you will need to do is supply the JSON schema and the file path you wish to save the output to.

```bash
jsf --schema jsf/tests/data/custom.json --instance wow.json
```

#### Docker

For convenience, you can also make use of the Docker image that is provided so there is no need to rely on package management.

```bash
docker build . -t challisa/jsf
docker run -v $PWD:/data challisa/jsf jsf --schema /data/jsf/tests/data/custom.json --instance /data/wow.json
```
