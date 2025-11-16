from database import SessionLocal, engine
from fastapi import Depends, FastAPI
from models import Base, Car, Family
from schemas import CarCreate, FamilyCreate
from sqlalchemy.orm import Session

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


@app.post("/families/")
def create_family(family: FamilyCreate, db: Session = Depends(get_db)):
    new_family = Family(name=family.name)
    db.add(new_family)
    db.commit()
    db.refresh(new_family)
    return new_family


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


@app.get("/families/{family_id}/cars")
def get_cars_from_family(family_id: int, db: Session = Depends(get_db)):
    # Verificar que la familia existe
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        return {"error": "Family not found"}

    # Acceso directo gracias a la relación ORM
    return family.cars
