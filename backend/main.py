from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]