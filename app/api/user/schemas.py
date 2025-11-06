from pydantic import BaseModel
import datetime

class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    signup_date: datetime.datetime