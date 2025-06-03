# app/models/user.py
from .base import Base  # relative import # not absolute ones (to helps avoid circular issues and improve modularity)
import enum

from sqlalchemy import func, Enum
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class ProfileType(enum.Enum):
    customer = 'customer'
    company = 'company'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    real_name = Column(String())
    username = Column(String())
    email = Column(String(), unique=True)
    phone_number = Column(Integer())
    password = Column(String())
    role = Column(String(), nullable=True) # changed
    profile_type = Column(Enum(ProfileType), default=ProfileType.customer) # customer, company, admin
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Relationships *Shipment moved
    services = relationship('Service', back_populates='user') # One-to-many relationship with Service
    provided_contact_infos = relationship("ShipmentContactInfo", back_populates="info_provider")


    # SQLAlchemy automatically provides a default constructor that accepts keyword arguments matching our model's attributes (columns and relationships). We'll exclude optional overriding __init__
    @classmethod
    def create(cls, session, **kwargs):
        user = cls(**kwargs) # no need for custom __init__
        session.add(user) # no session.commit(), context manager in lib will do that for us
        session.flush() # forcing sql insertion to get id
        return user

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_username_or_email(cls, session, keyword):
        return session.query(cls).filter(
            (cls.username == keyword) | (cls.email == keyword)
        ).first()

    @classmethod
    def delete_by_username(cls, session, username):
        user = session.query(cls).filter_by(username=username).first()
        if user:
            session.delete(user)
            return True
        return False
    
    def __repr__(self):
        return (f"User: id={self.id}" 
            f"Real_name={self.real_name}" 
            f"Username={self.username}" 
            f"Email={self.email}" 
            f"Phone_number={self.phone_number}" 
            f"Role={self.role}" 
            f"Profile_type={self.profile_type}")
