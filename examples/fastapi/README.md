# FastAPI Example

## Dependancies

* FastAPI
* uvicorn
* datamodel-code-generator

## Usage

Using `api.py` and `custom.json` in current example folder

```bash
datamodel-codegen --input src/tests/data/custom.json --output model.py
uvicorn api:app --reload --host 0.0.0.0 --port 8080
```
