# app/models/shipment.py
# from app.models.base import Base
from .base import Base  # relative import
from enum import Enum as PyEnum

from sqlalchemy import func, Enum
from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import relationship

class ShipmentStatus(PyEnum):
    pending = "pending"
    in_transit = "in transit"
    delivered = "delivered"

class ShipmentType(PyEnum):
    goods = "goods"
    person = "person"

class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id')) # Reference users table as shipments(attribute). User can have many shipments- through multiple rows
    origin_location_id = Column(Integer, ForeignKey('locations.id')) # many-to-one. In this column many rows may point to same origin_location_id. Many shipments can originate from one location
    destination_location_id = Column(Integer(), ForeignKey('locations.id'))
    route_id = Column(Integer, ForeignKey('routes.id'))
    service_id = Column(Integer(), ForeignKey('services.id'))
    status = Column(Enum(ShipmentStatus), nullable=False, default=ShipmentStatus.pending)  # pending, in transit, delivered
    shipment_type = Column(Enum(ShipmentType), default=ShipmentType.goods) # goods, person
    shipping_cost = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Relationships
    user = relationship('User', backref='shipments')
    service = relationship('Service', back_populates="shipments")
    origin = relationship('Location', foreign_keys=[origin_location_id], back_populates='shipments_originating') # disambiguate the FK column in the relationship since there are multiple FKs to the same table - Location.
    destination = relationship('Location', foreign_keys=[destination_location_id], back_populates='shipments_arriving') # simple unidirectional relationship since I don’t need a reverse relationship from target model - Locatn(back to shipment)
    route = relationship('Route', back_populates='shipments') # Many-to-one. One Shipment uses one Route. One Route can be used by many Shipments
    shipment_items = relationship('ShipmentItem', back_populates='shipment') #-Base rate on an item is available from its category(* no. of items)
    drop_logs = relationship('DropLog', back_populates='shipment')
    contact_info = relationship("ShipmentContactInfo", uselist=False, back_populates="shipment")

    @classmethod
    def create(cls, session, **kwargs):
        shipment = cls(**kwargs) # no need for custom __init__
        session.add(shipment) # no session.commit(), context manager in lib will do that for us
        session.flush()
        return shipment
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, shipment_id):
        try:
            shipment_id = int(shipment_id)
            return session.query(cls).filter_by(id=shipment_id).first()
        except ValueError:
            print("Invalid shipment ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, shipment_id):
        try:
            shipment_id = int(shipment_id)
        except ValueError:
            print("Invalid shipment ID.")
            return False

        shipment = session.query(cls).filter_by(id=shipment_id).first()
        if not shipment:
            return False

        session.delete(shipment)
        return True


    def __repr__(self):
        return (f"Shipment: id={self.id}"
            f"user_id={self.user_id}"
            f"origin_location_id={self.origin_location_id}"
            f"destination_location_id={self.destination_location_id}"
            f"route_id={self.route_id}"
            f"service_id={self.service_id}"
            f"status={self.status}"
            f"shipment_type={self.shipment_type}"
            f"shipping_cost={self.shipping_cost}")


