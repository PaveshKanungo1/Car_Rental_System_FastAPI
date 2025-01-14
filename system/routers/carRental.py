from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from system.database import get_db
from system.crud import create_user, get_user_by_username, delete_user_by_username, create_car, get_all_cars, get_car_by_id, update_car_status, create_rental, get_rentals_by_user_id, get_rentals_by_car_id, end_rental
from system.schemas import User as PydanticUser, Car as PydanticCar, RentalDetails as PydanticRental
from system.models import UserRole, CarStatus, User, Rental
from system.auth.oauth2 import get_current_user
from typing import List
from datetime import date

router = APIRouter()

@router.post("/admin/users/", response_model=PydanticUser, status_code=status.HTTP_201_CREATED)
def create_user_route(user: PydanticUser, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return create_user(db, user=user)


@router.delete("/admin/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(username: str, db: Session = Depends(get_db)):
    user = delete_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {username} deleted successfully"}


@router.get("/admin/users", response_model=List[PydanticUser])
def view_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/admin/cars/", response_model=PydanticCar, status_code=status.HTTP_201_CREATED)
def create_car_route(car: PydanticCar, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create a car",
        )

    return create_car(db, car=car)

@router.get("/cars", response_model=List[PydanticCar])
def view_all_cars_route(db: Session = Depends(get_db)):
    cars = get_all_cars(db)
    return cars

@router.get("/cars/{car_id}", response_model=PydanticCar)
def get_car_details_route(car_id: int, db: Session = Depends(get_db)):
    car = get_car_by_id(db, car_id=car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.put("/admin/cars/{car_id}/status", response_model=PydanticCar)
def update_car_status_route(car_id: int, status: CarStatus, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update a car",
        )

    car = update_car_status(db, car_id=car_id, status=status)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.post("/rentals/", response_model=PydanticRental, status_code=status.HTTP_201_CREATED)
def create_rental_route(rental: PydanticRental, current_user: PydanticUser = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.customer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only customers can rent cars")
    return create_rental(db, rental=rental)

@router.get("/rentals/user", response_model=List[PydanticRental])
def view_rentals_by_user_route(current_user: PydanticUser = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.customer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only customers can view their rentals")
    rentals = get_rentals_by_user_id(db, user_id=current_user.id)
    return rentals

@router.get("/rentals/car/{car_id}", response_model=List[PydanticRental])
def view_rentals_by_car_route(car_id: int, db: Session = Depends(get_db)):
    rentals = get_rentals_by_car_id(db, car_id=car_id)
    if not rentals:
        raise HTTPException(status_code=404, detail="No rentals found for this car")
    return rentals

@router.put("/rentals/{rental_id}/end", response_model=PydanticRental)
def end_rental_route(rental_id: int, return_date: date, current_user: PydanticUser = Depends(get_current_user), db: Session = Depends(get_db)):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    
    if rental.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to end this rental")

    return end_rental(db, rental_id=rental_id, return_date=return_date)
