# app/models/route_group.py
from .base import Base  # relative import

from sqlalchemy import func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class RouteGroup(Base): # not a bridge, but enable route grouping through SQLAlchemy relationships(route_group_id in routes allow this)
    __tablename__ = 'route_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)  # e.g., "Nairobi Metro", "Eldoret Express", "Kilifi routes"
    description = Column(String, nullable=True)
    region_location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)  # Optional anchor location/central location/HQ # This is added to 'enrich' the RouteGroup, any other model could be

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Relationships
    region_location = relationship("Location", back_populates="route_groups")  # Optional
    routes = relationship("Route", back_populates="route_group")

    @classmethod
    def create(cls, session, **kwargs):
        route_group = cls(**kwargs) 
        session.add(route_group) 
        session.flush()
        return route_group
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, route_group_id):
        try:
            route_group_id = int(route_group_id)
            return session.query(cls).filter_by(id=route_group_id).first()
        except ValueError:
            print("Invalid route group ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, route_group_id):
        try:
            route_group_id = int(route_group_id)
        except ValueError:
            print("Invalid route group ID.")
            return False

        route_group = session.query(cls).filter_by(id=route_group_id).first()
        if not route_group:
            return False

        session.delete(route_group)
        return True

    def __repr__(self):
        return (f"RouteGroup: id={self.id}"
            f"name={self.name}"
            f"description={self.description}"
            f"region_location_id={self.region_location_id}"
            f"created_at={self.created_at}"
            f"updated_at={self.updated_at}")
