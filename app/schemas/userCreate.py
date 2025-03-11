from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    last_name: str
    phone: int
    address: str
    name_contac_emerg: str
    phone_contac_emerg: int
    email: str
    password: str
