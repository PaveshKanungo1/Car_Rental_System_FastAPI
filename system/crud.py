from sqlalchemy.orm import Session
from system.models import User, Car, Rental
from system.schemas import User as PydanticUser, Car as PydanticCar, RentalDetails as PydanticRental
from datetime import date
from system.auth.hashing import get_password_hash

def create_user(db:Session, user: PydanticUser):
    db_user = User(username=user.username, password=get_password_hash(user.password), role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def delete_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def create_car(db: Session, car: PydanticCar):
    db_car = Car(
        make=car.make,
        model=car.model,
        year=car.year,
        status=car.status
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def get_all_cars(db: Session):
    return db.query(Car).all()

def get_car_by_id(db: Session, car_id: int):
    return db.query(Car).filter(Car.id == car_id).first()

def update_car_status(db: Session, car_id: int, status: str):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car:
        car.status = status
        db.commit()
        db.refresh(car)
    return car

def create_rental(db: Session, rental: PydanticRental):
    db_rental = Rental(
        car_id=rental.car_id,
        user_id=rental.user_id,
        rental_date=rental.rental_date,
        return_date=rental.return_date
    )
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    return db_rental

def get_rentals_by_user_id(db: Session, user_id: int):
    return db.query(Rental).filter(Rental.user_id == user_id).all()

def get_rentals_by_car_id(db: Session, car_id: int):
    return db.query(Rental).filter(Rental.car_id == car_id).all()

def end_rental(db: Session, rental_id: int, return_date: date):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if rental:
        rental.return_date = return_date
        db.commit()
        db.refresh(rental)
    return rental
