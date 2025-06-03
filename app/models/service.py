# app/models/service.py
from .base import Base  # relative import

from sqlalchemy import func 
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    company_name = Column(String())
    service_name = Column(String())
    cost = Column(Integer())
    license = Column(String())
    image_url = Column(String(), nullable=True)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    user = relationship("User", back_populates="services")
    shipments = relationship("Shipment", back_populates="service")

    @classmethod
    def create(cls, session, **kwargs):
        service = cls(**kwargs) 
        session.add(service) 
        session.flush()
        return service
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, service):
        try:
            service = int(service)
            return session.query(cls).filter_by(id=service).first()
        except ValueError:
            print("Invalid service info ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, service_id):
        try:
            service_id = int(service_id)
        except ValueError:
            print("Invalid service info ID.")
            return False

        service = session.query(cls).filter_by(id=service_id).first()
        if not service:
            return False

        session.delete(service)
        return True