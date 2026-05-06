import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session
from models import CustomerRequest, RequestClassification

load_dotenv()

DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(DATABASE_URL,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def save_customer_request(request_data:CustomerRequest):
    with Session(engine) as session:
        session.add(request_data)
        session.commit()
        session.refresh(request_data)
        return request_data
    
def save_classification(classification_data:RequestClassification):
    with Session(engine) as session:
        session.add(classification_data)
        session.commit()
        session.refresh(classification_data)
        return classification_data
