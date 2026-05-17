from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, JSON, Column
from pydantic import BaseModel


class CustomerRequest(SQLModel,table = True):
    __tablename__ = "customer_requests"
    id : Optional[int] = Field(default=None,primary_key=True)
    ticket_id: str = Field(index=True, unique=True)
    customer_id : str 
    channel : str 
    request_text: str
    created_at: datetime

class RequestClassification(SQLModel,table=True):
    __tablename__ = "request_classifications"
    id : Optional[int] = Field(default=None,primary_key=True)
    ticket_id : str = Field(index=True)
    category : str 
    priority : str 
    tags : List[str] = Field(sa_column=Column(JSON))
    estimated_resolution_time : int 
    confidence : float 
    processed_at : datetime = Field(default_factory=datetime.now)


class ClassificationResult(BaseModel):
    category : str 
    priority:str 
    tags : List[str]
    estimated_resolution_time : int
    confidence : float

