# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud import get_all_items, create_item, get_item_by_id, update_item_by_id, delete_item_by_id
from database import get_db
from exceptions import ItemException
from schemas import Item, CreateAndUpdateItem, PaginatedItem, ItemWithMessage, MessageOnly

router = APIRouter()


# Example of Class based view
@cbv(router)
class Items:
    session: Session = Depends(get_db)

    # API to get the list of item info
    @router.get("/items", response_model=PaginatedItem)
    def list_items(self, limit: int = 10, offset: int = 0):

        items_list = get_all_items(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": items_list, "message": "Items fetched successfully."}

        return response

    # API endpoint to add a item info to the database
    @router.post("/add-item", response_model=ItemWithMessage)
    def add_item(self, item: CreateAndUpdateItem):

        try:
            item = create_item(self.session, item)
            return {"data": item, "message": "Item added successfully."}
        except ItemException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular item
@router.get("/item/{item_id}", response_model=ItemWithMessage)
def get_item(item_id: int, session: Session = Depends(get_db)):

    try:
        item = get_item_by_id(session, item_id)
        return {"data": item, "message": "Item fetched successfully with id {}.".format(item_id)}
    except ItemException as cie:
        raise HTTPException(**cie.__dict__)


# API to update a existing item
@router.put("/update-item/{item_id}", response_model=ItemWithMessage)
def update_item(item_id: int, new_info: CreateAndUpdateItem, session: Session = Depends(get_db)):
    try:
        item = update_item_by_id(session, item_id, new_info)
        return {"data": item, "message": "Item updated successfully with id {}.".format(item_id)}
    except ItemException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a item from the data base
@router.delete("/delete-item/{item_id}", response_model=MessageOnly)
def delete_item(item_id: int, session: Session = Depends(get_db)):

    try:
        delete_item_by_id(session, item_id)
        return {"message": "Item deleted successfully with id {}.".format(item_id)}
    except ItemException as cie:
        raise HTTPException(**cie.__dict__)
