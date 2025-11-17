from fastapi import FastAPI
import uvicorn
app = FastAPI()

#@app.get("/items/{item_id}")
#def read_item(item_id: int):
#    return {"item_id": item_id}

#@app.get("/")
#def root():
   # return {"message": "Welcome to the FastAPI application!"}

#path parameters
#@app.get("/users/{user_id}")
#def get_user(user_id: int):
 #   return {"user_id": user_id, "name": f"John Doe"}

#@app.get("/items/")
#def get_items(skip: int= 0, limit: int=10):
  #  return{"skip": skip, "limit": limit}

#GET method with query parameters
@app.get("/items/")
def read_item():
    return{"items": ["item1", "item2", "item3"]}

#POST method
@app.post("/items/")
def create_item(name: str, price: float):
    return{"item_name": name, "item_price": price}

#PUT method
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    return{"item_id": item_id, "item_name": name, "item_price": price}

#DELETE method
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return{"message": f"Item with id {item_id} has been deleted"}


