# app/models/shipmentContactInfo.py
from .base import Base  # relative import

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class ShipmentContactInfo(Base):
    __tablename__ = "shipments_contact_info"

    id = Column(Integer, primary_key=True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'), nullable=False)
    
    sender_name = Column(String, nullable=False)
    sender_phone = Column(String, nullable=False)
    sender_address = Column(String, nullable=False)

    receiver_name = Column(String, nullable=False)
    receiver_phone = Column(String, nullable=False)
    receiver_address = Column(String, nullable=False)

    info_provider_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    shipment = relationship("Shipment", back_populates="contact_info")  # Reciprocal relationship in Shipment
    info_provider = relationship("User", back_populates="provided_contact_infos")  # Reciprocal relationship in User

    @classmethod
    def create(cls, session, **kwargs):
        shipment_contact_info = cls(**kwargs) 
        session.add(shipment_contact_info) 
        session.flush()
        return shipment_contact_info
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, shipment_contact_info_id):
        try:
            shipment_contact_info_id = int(shipment_contact_info_id)
            return session.query(cls).filter_by(id=shipment_contact_info_id).first()
        except ValueError:
            print("Invalid shipment contact info ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, shipment_contact_info_id):
        try:
            shipment_contact_info_id = int(shipment_contact_info_id)
        except ValueError:
            print("Invalid shipment contact info ID.")
            return False

        shipment_contact_info = session.query(cls).filter_by(id=shipment_contact_info_id).first()
        if not shipment_contact_info:
            return False

        session.delete(shipment_contact_info)
        return True
