from fastapi import FastAPI
from system.database import Base, engine 
from system.routers import carRental as car_rental
from system.auth.oauth2 import get_current_user 
from system.auth.oauth2 import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(car_rental.router, prefix="/api", tags=["Car Rental"]) 
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
