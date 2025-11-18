from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Item
from app.schemas.user import ItemCreate, ItemUpdate
from app.utils.exceptions import NotFoundException

class ItemService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_item(self, item_create: ItemCreate, owner_id: int) -> Item:
        db_item = Item(
            title=item_create.title,
            description=item_create.description,
            owner_id=owner_id
        )
        
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def get_item(self, item_id: int) -> Item:
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise NotFoundException("Item", item_id)
        return item
    
    def get_items_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.db.query(Item).filter(Item.owner_id == owner_id).offset(skip).limit(limit).all()
    
    def get_all_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.db.query(Item).offset(skip).limit(limit).all()
    
    def update_item(self, item_id: int, item_update: ItemUpdate) -> Item:
        item = self.get_item(item_id)
        
        update_data = item_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(item, field, value)
        
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete_item(self, item_id: int) -> bool:
        item = self.get_item(item_id)
        self.db.delete(item)
        self.db.commit()
        return True