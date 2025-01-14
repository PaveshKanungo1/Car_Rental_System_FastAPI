from sqlalchemy import Column, Integer, String, Boolean, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from system.database import Base
import enum

class UserRole(enum.Enum):
    customer = "customer"
    admin = "admin"

class CarStatus(enum.Enum):
    available = "available"
    rented = "rented"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    rentals = relationship("Rental", back_populates="user")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Enum(CarStatus), default=CarStatus.available, nullable=False)

    rentals = relationship("Rental", back_populates="car")

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rental_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    car = relationship("Car", back_populates="rentals")
    user = relationship("User", back_populates="rentals")