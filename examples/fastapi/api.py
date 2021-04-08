from jsf import JSF
from fastapi import FastAPI

from model import Model

app = FastAPI()


@app.get("/", response_model=Model)
def read_root():
    return JSF.from_json("custom.json").generate()
