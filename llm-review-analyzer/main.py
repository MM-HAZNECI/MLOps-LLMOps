from fastapi import FastAPI
from routers.llm import llm_ep 
from database import create_db_and_tables 

app = FastAPI(title="LLM Review API")

app.include_router(llm_ep.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()