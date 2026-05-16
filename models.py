from typing import Optional
from sqlmodel import SQLModel, Field



class Customer(SQLModel, table=True):
    customerId: Optional[int] = Field(default=None, primary_key=True)
    customerFName: str
    customerLName: str
    customerEmail: str
    customerPassword: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str



class CreateCustomer(SQLModel):
    customerFName: str
    customerLName: str
    customerEmail: str
    customerPassword: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str



class UpdateCustomer(SQLModel):
    customerFName: Optional[str] = None
    customerLName: Optional[str] = None
    customerEmail: Optional[str] = None
    customerPassword: Optional[str] = None
    customerStreet: Optional[str] = None
    customerCity: Optional[str] = None
    customerState: Optional[str] = None
    customerZipcode: Optional[str] = None



class ShowCustomer(SQLModel):
    customerId: int
    customerFName: str
    customerLName: str
    customerEmail: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str