# app/models/shipmentItem.py
# from app.models.base import Base
from .base import Base  # relative import

from sqlalchemy import func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship

class ShipmentItem(Base):
    __tablename__ = 'shipment_items'

    id = Column(Integer, primary_key=True)
    shipment_id = Column(Integer(), ForeignKey('shipments.id'))
    item_name = Column(String())
    description = Column(Text)
    weight = Column(Float)
    quantity = Column(Integer())
    value = Column(Integer())
    category_id = Column(Integer(), ForeignKey('item_categories.id')) # also check base rate for the category

    shipment = relationship('Shipment', back_populates='shipment_items')
    category = relationship("ItemCategory", back_populates="shipment_items")

    @classmethod
    def create(cls, session, **kwargs):
        shipment_item = cls(**kwargs) 
        session.add(shipment_item) 
        session.flush()
        return shipment_item
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, shipment_item_id):
        try:
            shipment_item_id = int(shipment_item_id)
            return session.query(cls).filter_by(id=shipment_item_id).first()
        except ValueError:
            print("Invalid shipment item ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, shipment_item_id):
        try:
            shipment_item_id = int(shipment_item_id)
        except ValueError:
            print("Invalid shipment item ID.")
            return False

        shiping_cost_item = session.query(cls).filter_by(id=shipment_item_id).first()
        if not shiping_cost_item:
            return False

        session.delete(shiping_cost_item)
        return True