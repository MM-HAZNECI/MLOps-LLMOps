from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from passlib.context import CryptContext

from db import create_db_and_tables, get_db
from models import Customer, CreateCustomer, UpdateCustomer, ShowCustomer

app = FastAPI(title="Retail Customers API")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Yeni müşteri ekle
@app.post("/customers", status_code=status.HTTP_201_CREATED, response_model=ShowCustomer)
def create_customer(request: CreateCustomer, session: Session = Depends(get_db)):
    new_customer = Customer(
        customerFName=request.customerFName,
        customerLName=request.customerLName,
        customerEmail=request.customerEmail,
        customerPassword=hash_password(request.customerPassword),
        customerStreet=request.customerStreet,
        customerCity=request.customerCity,
        customerState=request.customerState,
        customerZipcode=request.customerZipcode
    )
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer


# Tüm müşterileri listele (city ve limit filtresi)
@app.get("/customers", status_code=status.HTTP_200_OK, response_model=List[ShowCustomer])
def get_all_customers(
    city: Optional[str] = None,
    limit: Optional[int] = None,
    session: Session = Depends(get_db)
):
    query = select(Customer)
    if city:
        query = query.where(Customer.customerCity == city)
    if limit:
        query = query.limit(limit)
    customers = session.exec(query).all()
    return customers


# ID'ye göre müşteri getir
@app.get("/customers/{id}", status_code=status.HTTP_200_OK, response_model=ShowCustomer)
def get_customer(id: int, session: Session = Depends(get_db)):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {id} not found."
        )
    return customer


#  Müşteri güncelle
@app.put("/customers/{id}", status_code=status.HTTP_200_OK, response_model=ShowCustomer)
def update_customer(id: int, request: UpdateCustomer, session: Session = Depends(get_db)):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {id} not found."
        )
    update_data = request.dict(exclude_unset=True)
    if "customerPassword" in update_data:
        update_data["customerPassword"] = hash_password(update_data["customerPassword"])
    for key, value in update_data.items():
        setattr(customer, key, value)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


#  Müşteri sil
@app.delete("/customers/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id: int, session: Session = Depends(get_db)):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {id} not found."
        )
    session.delete(customer)
    session.commit()