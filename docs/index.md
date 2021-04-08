## Installation

```bash
pip install jsf
```

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
