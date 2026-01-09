from pydantic import BaseModel,Field

class CreateUserRequest(BaseModel):
    username :str
    email : str
    hash_password : str
    admin : bool
    first_name :str
    lastaname :str
    is_active :bool

class UserLogin(BaseModel):
    username: str
    password: str