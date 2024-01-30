---
hide:
  - navigation
---

# jsf Features

**jsf** gives you the following:

## Based on open standards

- Provides out of the box data generation from any [JSON schema](https://json-schema.org/) 📦
- In memory conversion from [JSON Schema](https://json-schema.org/) to [Pydantic](https://docs.pydantic.dev/latest/) Models with generated examples 🤯
- Inbuilt validation of fake JSON produced against the [JSON schema](https://json-schema.org/) ✅
  
## Ability to extend the standard to maximize realness of the fake data

- Extendable custom data providers using any lambda functions 🔗
- Multi level state for dependant data (eg multiple objects sharing value, such as children with same surname) 🤓

## Plug and play

- Seamless integration with [FastAPI](https://fastapi.tiangolo.com/), check out the [demo code](https://github.com/ghandic/jsf/tree/main/examples/fastapi) 🚀
- Standardize on JSON schema and output to any file format, check out the [demo code](https://github.com/ghandic/jsf/tree/main/examples/flatfile) 📦
