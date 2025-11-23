from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    cars = relationship("Car", back_populates="family", cascade="all, delete")
    access = relationship("UserAccess", back_populates="family")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    id_family = Column(Integer, ForeignKey("families.id"), nullable=False)
    name = Column(String(100), nullable=False)

    family = relationship("Family", back_populates="cars")


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    access = relationship("UserAccess", back_populates="user")


class UserAccess(Base):
    __tablename__ = "user_access"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_info.id"))
    family_id = Column(Integer, ForeignKey("families.id"))

    user = relationship("UserInfo", back_populates="access")
    family = relationship("Family", back_populates="access")
