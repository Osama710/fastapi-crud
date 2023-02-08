# crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions import ItemAlreadyExistError, ItemNotFoundError
from models import Item
from schemas import CreateAndUpdateItem


# Function to get list of car info
def get_all_items(session: Session, limit: int, offset: int) -> List[Item]:
    return session.query(Item).offset(offset).limit(limit).all()


# Function to  get info of a particular item
def get_item_by_id(session: Session, _id: int) -> Item:
    item_info = session.query(Item).get(_id)

    if item_info is None:
        raise ItemNotFoundError

    return item_info


# Function to add a new item info to the database
def create_item(session: Session, item: CreateAndUpdateItem) -> Item:
    item_details = session.query(Item).filter(Item.name == item.name, Item.description == item.description).first()
    if item_details is not None:
        raise ItemAlreadyExistError

    new_item = Item(**item.dict())
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item


# Function to update details of the item
def update_item_by_id(session: Session, _id: int, item_update:CreateAndUpdateItem) -> Item:
    item = get_item_by_id(session, _id)

    if item is None:
        raise ItemNotFoundError

    for key, value in item_update.dict().items():
        if value is not None:
            setattr(item, key, value)

    session.commit()
    session.refresh(item)

    return item


# Function to delete an item from the db
def delete_item_by_id(session: Session, _id: int):
    item = get_item_by_id(session, _id)

    if item is None:
        raise ItemNotFoundError

    session.delete(item)
    session.commit()

    return
