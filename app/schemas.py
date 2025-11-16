from pydantic import BaseModel


class FamilyCreate(BaseModel):
    name: str


class CarCreate(BaseModel):
    id_family: int
    name: str
