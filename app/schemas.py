from pydantic import BaseModel


class FamilyCreate(BaseModel):
    name: str


class CarCreate(BaseModel):
    id_family: int
    name: str


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class UserAccessCreate(BaseModel):
    user_id: int
    family_id: int
