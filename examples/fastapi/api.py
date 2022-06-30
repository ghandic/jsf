from fastapi import FastAPI

from jsf import JSF

app = FastAPI(docs_url="/")
generator = JSF.from_json("custom.json")


@app.get("/generate", response_model=generator.pydantic())
def read_root():
    return generator.generate()
