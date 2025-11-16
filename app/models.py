from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    cars = relationship("Car", back_populates="family")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    id_family = Column(Integer, ForeignKey("families.id"), nullable=False)
    name = Column(String(100), nullable=False)

    family = relationship("Family", back_populates="cars")
