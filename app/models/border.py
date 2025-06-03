# app/models/border.py
# from app.models.base import Base
from .base import Base  # relative import
import enum

from sqlalchemy import func, Enum
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

class BorderType(enum.Enum):
    intra_city = "intra_city"
    inter_city = "inter_city"
    inter_county = "trans_county"
    trans_county = "trans_county"
    cross_country = "cross_country"

class BorderStatus(enum.Enum):
    open = "open"
    closed = "closed"
    restricted = "restricted"

class Border(Base):
    __tablename__ = 'borders'
    id = Column(Integer(), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'), unique=True)
    border_type = Column(Enum(BorderType), nullable=False)
    checkpoint_name = Column(String(), nullable=False) # e.g. "Namanga Border
    status = Column(Enum(BorderStatus))
    notes = Column(Text)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    location = relationship("Location", back_populates="border_info") # border provide info about location

    @classmethod
    def create(cls, session, **kwargs):
        border = cls(**kwargs) 
        session.add(border) 
        session.flush()
        return border
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, border_id):
        try:
            border_id = int(border_id)
            return session.query(cls).filter_by(id=border_id).first()
        except ValueError:
            print("Invalid border ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, border_id):
        try:
            border_id = int(border_id)
        except ValueError:
            print("Invalid border ID.")
            return False

        border = session.query(cls).filter_by(id=border_id).first()
        if not border:
            return False

        session.delete(border)
        return True