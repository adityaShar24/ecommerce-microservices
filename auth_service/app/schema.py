from pydantic import BaseModel , EmailStr

class UserCreate(BaseModel):
    full_name : str
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    full_name: str
    email : EmailStr

    class Config:
        orm_mode = True

    
class UserLogin(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str = 'bearer'