from fastapi import FastAPI
from app import models
from app.database import engine

app=FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"status":"Expense and profit analyser is alive"}

@app.get("/health")
def health():
    return {"status": "ok"}