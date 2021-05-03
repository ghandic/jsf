from jsf import JSF
from fastapi import FastAPI

app = FastAPI(docs_url="/")
generator = JSF.from_json("custom.json")


@app.get("/generate", response_model=generator.pydantic())
def read_root():
    return generator.generate()
