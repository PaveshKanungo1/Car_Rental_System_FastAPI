import pytest
from sqlalchemy import create_engine
from system.database import Base, SessionLocal
from sqlalchemy.orm import sessionmaker
from system.models import User, UserRole, CarStatus, Rental
from fastapi.testclient import TestClient
from system.schemas import User as PydanticUser, Car as PydanticCar, RentalDetails as PydanticRental
from system.main import app
from datetime import date

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)

    db_session = TestingSessionLocal()

    yield db_session

    db_session.close()
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def new_user_data():
    return {
        "username": "pavesh",
        "password": "12345",
        "role": 'customer'
    }

def test_create_user(db, new_user_data):
    user = User(**new_user_data)
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.username == new_user_data["username"]
    # print(user.__dict__)
    assert user.role.value == new_user_data["role"]


def create_user(db, user_data):
    user = User(username=user_data["username"],password=user_data["password"], role=UserRole(user_data["role"]))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user_by_username(db, user_data):
    user = db.query(User).filter(User.username == user_data['username']).first()
    
    if user:
        db.delete(user)
        db.commit()

    return user is not None

@pytest.fixture
def delete_user_data():
    return {
        "username": "pavesh",
        "password": "12345",
        "role": "customer"
    }

def test_delete_user(db, delete_user_data):
    # print(type(delete_user_data))
    user = create_user(db, user_data=delete_user_data)
    delete_user_by_username(db, delete_user_data['username'])
    
    db_user = db.query(User).filter(User.username == delete_user_data["username"]).first()
    assert db_user is None





