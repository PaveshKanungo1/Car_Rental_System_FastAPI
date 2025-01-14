from pydantic import BaseModel, model_validator
from typing import Optional, List
from datetime import date, datetime
import enum

class UserRole(str, enum.Enum):
    customer = "customer"
    admin = "admin"

class CarStatus(str, enum.Enum):
    available = "available"
    rented = "rented"

class UserBase(BaseModel):
    username: str
    role: UserRole
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
    
class CarBase(BaseModel):
    make: str
    model: str
    year: int

class Car(CarBase):
    id: int
    status: CarStatus = CarStatus.available

    class Config:
        orm_mode = True

class RentalDetails(BaseModel):
    car_id: int
    user_id: int
    rental_date: date
    return_date: Optional[date] = None

    @model_validator(mode='before')
    def validate_dates(cls, values):
        rental_date = values.get("rental_date")
        return_date = values.get("return_date")
        if return_date and return_date < rental_date:
            raise ValueError("Return date cannot be before rental date.")
        return values
    
class ShowCar(BaseModel):
    make: str
    model: str
    year: int
    status: CarStatus

    class Config: 
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    role: UserRole

    class Config:
        orm_mode = True

class ShowRentalDetails(BaseModel):
    car: ShowCar
    user: ShowUser
    rental_date: date
    return_date: Optional[date] = None

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


