from pydantic import BaseModel, conint, constr
from typing import Optional

#class User(BaseModel):
#    id: int
#    name: str
#    age: int
 #   email: str

#validation

#user = User(id=1, name="John Doe", age=24, email="johndoe@example.com")

#default values and optional fields
class User(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    email: Optional[str] = None

user1 = User(id=1, name="John", age=30, email="")
print(user1)

user2 = User(id=2, name="Pork", age=None, email="jane@example.com")
print(user2)

user3 = User(id=3, name="Alice", age=30)
print(user3)

user4 = User(id=4, name="Bob", age=30, email="")
print(user4)

#field constraints
class another_model(BaseModel):
    id: conint(gt=0)
    name: constr(min_length=3, max_length=50)

valid_user= another_model(id=1, name="Alice")
print(valid_user)

invalid_user= another_model(id=0, name="Bob")
print(invalid_user)