# app/models/ItemCategory.py
# from app.models.base import Base
from .base import Base  # relative import

from sqlalchemy import func
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import relationship

class ItemCategory(Base):
    __tablename__ = 'item_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    base_rate = Column(Float, default=1.0) # base rate for a category
    description = Column(Text)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    shipment_items = relationship("ShipmentItem", back_populates="category")

    @classmethod
    def create(cls, session, **kwargs):
        item_category = cls(**kwargs) 
        session.add(item_category) 
        session.flush()
        return item_category
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, item_category_id):
        try:
            item_category_id = int(item_category_id)
            return session.query(cls).filter_by(id=item_category_id).first()
        except ValueError:
            print("Invalid item category ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, item_category_id):
        try:
            item_category_id = int(item_category_id)
        except ValueError:
            print("Invalid item category ID.")
            return False

        item_category = session.query(cls).filter_by(id=item_category_id).first()
        if not item_category:
            return False

        session.delete(item_category)
        return True

