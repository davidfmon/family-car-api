from database import SessionLocal, engine
from fastapi import Depends, FastAPI
from models import Base, Car, Family, UserAccess, UserInfo
from passlib.context import CryptContext
from schemas import CarCreate, FamilyCreate, UserAccessCreate, UserCreate, UserResponse
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)


# Dependencia para obtener sesion DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # ¿Existe email?
    existing = db.query(UserInfo).filter(UserInfo.email == user.email).first()
    if existing:
        return {"error": "Email already in use"}

    hashed_password = pwd_context.hash(user.password)

    new_user = UserInfo(name=user.name, email=user.email, password_hash=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/families/")
def create_family(family: FamilyCreate, db: Session = Depends(get_db)):
    new_family = Family(name=family.name)
    db.add(new_family)
    db.commit()
    db.refresh(new_family)
    return new_family


@app.delete("/families/{family_id}")
def delete_family(family_id: int, db: Session = Depends(get_db)):
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        return {"error": "Family not found"}

    db.delete(family)
    db.commit()
    return {"message": f"Family {family_id} deleted"}


@app.post("/cars/")
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    # Comprobar que la familia existe
    family = db.query(Family).filter(Family.id == car.id_family).first()
    if not family:
        return {"error": "Family does not exist"}

    new_car = Car(id_family=car.id_family, name=car.name)
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return {"error": "Car not found"}

    db.delete(car)
    db.commit()
    return {"message": f"Car {car_id} deleted"}


@app.get("/families/{family_id}/cars")
def get_cars_from_family(family_id: int, db: Session = Depends(get_db)):
    # Verificar que la familia existe
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        return {"error": "Family not found"}

    # Acceso directo gracias a la relación ORM
    return family.cars


@app.post("/users/access")
def give_user_family_access(data: UserAccessCreate, db: Session = Depends(get_db)):
    # Verificar usuario
    user = db.query(UserInfo).filter(UserInfo.id == data.user_id).first()
    if not user:
        return {"error": "User not found"}

    # Verificar familia
    family = db.query(Family).filter(Family.id == data.family_id).first()
    if not family:
        return {"error": "Family not found"}

    # Evitar duplicados
    existing = (
        db.query(UserAccess)
        .filter(
            UserAccess.user_id == data.user_id, UserAccess.family_id == data.family_id
        )
        .first()
    )

    if existing:
        return {"message": "User already has access to this family"}

    access = UserAccess(user_id=data.user_id, family_id=data.family_id)
    db.add(access)
    db.commit()

    return {"message": "Access granted"}
