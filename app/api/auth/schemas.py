from pydantic import BaseModel
import datetime

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    signup_date: datetime.datetime

class UserRegister(BaseModel):
    username: str
    email: str
    password: str