from fastapi import FastAPI , Path , Query
from typing import Optional
from pydantic import BaseModel
import uvicorn


app = FastAPI()

class Item(BaseModel) : 
  name : str
  price : float
  brand : Optional[str] = None
  
class UpdateItem(BaseModel) : 
  name : Optional[str] = None
  price : Optional[float] = None
  brand : Optional[str] = None
  
## GET METHOD
@app.get("/")
def home() :
  return{"Data" : "Testing"}

@app.get("/about")
def about() :
  return {"Data" : "About"}

# inventory = {
#   1 : {
#     "name" : "Milk" , 
#     "price" : 3.99 , 
#     "brand" : "Regular"
#   }
# }
## 

inventory = {}
##Path Parameter
@app.get("/get-item/{item_id}")
def get_item(item_id : int = Path(description = "The ID of the item to view"   , gt = 0) ) :
  return inventory[item_id]

## Query Parameter comes after ?
## http://127.0.0.1:8000/get-by-name?test=2&name=Milk
@app.get("/get-by-name")
def get_item(name : str = Query(None , title = "Name" , description = "Item name")) :
 for item_id in inventory : 
   if inventory[item_id].name == name:
     return inventory[item_id]  
 return {"Data" : "Not found"}

## Combine path and query parameter
## http://127.0.0.1:8000/get-by-name-id/1?test=2&name=Milk
@app.get("/get-by-name-id/{item_id}")
def get_item(item_id:int , test : int , name : Optional[str] = None) :
 for item in inventory :
  #  if item == item_id : 
  #   if inventory[item]["name"] == name:
  #    return inventory[item_id] 
    if item == item_id : 
      if inventory[item].name == name:
        return inventory[item_id]  
 return {"Data" : "Not found"}

## Request body
@app.post("/create-item/{item_id}")
def create_item(item_id : int , item : Item) : 
  if item_id in inventory : 
    return {"Error" : "Item id aldready exists"}
  
  # inventory[item_id] = {
  #   "name" : item.name , 
  #   "brand" : item.brand , 
  #   "price" : item.price
  # }
  
  inventory[item_id] = item
  
  return inventory[item_id]

##Update query
@app.put("/update-item/{item_id}")
def update_item(item_id : int , item : UpdateItem) :
  if item_id not in inventory : 
    return {"Error" : "Item id does not exists"}

  if item.name != None : 
    inventory[item_id].name = item.name
    
  if item.price != None : 
    inventory[item_id].price = item.price

  if item.brand != None : 
    inventory[item_id].brand = item.brand
      
  return inventory[item_id]

## delete method
@app.delete("/delete-item")
def delete_item(item_id : int = Query(... , description = "ID of item to delete" , gt = 0 , lt = 1000)) :
  if item_id not in inventory : 
    return {"Error" : "ID does not exist"}
  
  del inventory[item_id]
  return {"Success" : "Item deleted" }
  