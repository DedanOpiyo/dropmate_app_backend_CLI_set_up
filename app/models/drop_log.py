# app/models/drop_log.py
# from app.models.base import Base
from .base import Base  # relative import
from enum import Enum as PyEnum

from sqlalchemy import func, Enum 
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class DropLogStatus(PyEnum):
    scheduled = "scheduled"
    in_progress = "in progress"
    completed = "completed"

class DropLog(Base):
    __tablename__ = 'drop_logs'
    id = Column(Integer, primary_key=True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'))
    status = Column(Enum(DropLogStatus), nullable=False, default=DropLogStatus.scheduled)
    location = Column(String)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    shipment = relationship("Shipment", back_populates="drop_logs")

    @classmethod
    def create(cls, session, **kwargs):
        drop_log = cls(**kwargs) 
        session.add(drop_log) 
        session.flush()
        return drop_log
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, drop_log_id):
        try:
            drop_log_id = int(drop_log_id)
            return session.query(cls).filter_by(id=drop_log_id).first()
        except ValueError:
            print("Invalid drop log ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, drop_log_id):
        try:
            drop_log_id = int(drop_log_id)
        except ValueError:
            print("Invalid drop log ID.")
            return False

        drop_log = session.query(cls).filter_by(id=drop_log_id).first()
        if not drop_log:
            return False

        session.delete(drop_log)
        return True