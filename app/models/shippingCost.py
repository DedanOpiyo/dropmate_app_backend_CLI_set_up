# app/models/shippingCost.py
# from app.models.base import Base
from .base import Base  # relative import

from sqlalchemy import func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

class ShippingCost(Base):
    __tablename__ = 'shipping_costs'

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.id'), unique=True) # enforce uniqueness to define one-to-one relationship
    cost_value = Column(Integer)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    route = relationship("Route", back_populates="shipping_cost")

    @classmethod
    def create(cls, session, **kwargs):
        shipping_cost = cls(**kwargs) 
        session.add(shipping_cost) 
        session.flush()
        return shipping_cost
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, shipping_cost_id):
        try:
            shipping_cost_id = int(shipping_cost_id)
            return session.query(cls).filter_by(id=shipping_cost_id).first()
        except ValueError:
            print("Invalid shipping cost ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, shipping_cost_id):
        try:
            shipping_cost_id = int(shipping_cost_id)
        except ValueError:
            print("Invalid shipment cost ID.")
            return False

        shiping_cost = session.query(cls).filter_by(id=shipping_cost_id).first()
        if not shiping_cost:
            return False

        session.delete(shiping_cost)
        return True