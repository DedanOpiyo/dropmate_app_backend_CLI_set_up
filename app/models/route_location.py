# app/models/route_location.py
from .base import Base  # relative import

from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship

class RouteLocation(Base):
    __tablename__ = 'route_locations'

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    sequence = Column(Integer)

    route = relationship("Route", back_populates="route_locations")
    location = relationship("Location", back_populates="route_locations")

    @classmethod
    def create(cls, session, **kwargs):
        route_location = cls(**kwargs) 
        session.add(route_location) 
        session.flush()
        return route_location
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, route_location_id):
        try:
            route_location_id = int(route_location_id)
            return session.query(cls).filter_by(id=route_location_id).first()
        except ValueError:
            print("Invalid route location ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, route_location_id):
        try:
            route_location_id = int(route_location_id)
        except ValueError:
            print("Invalid route location ID.")
            return False

        route_location = session.query(cls).filter_by(id=route_location_id).first()
        if not route_location:
            return False

        session.delete(route_location)
        return True