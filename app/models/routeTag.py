# app/models/routeTag.py
# from app.models.base import Base
from .base import Base  # relative import

from sqlalchemy import func
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

class RouteTag(Base):
    __tablename__ = 'route_tags'

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    tag = Column(String, nullable=False)
    price_factor = Column(Float, default=1.0)

    route = relationship('Route', back_populates='tags')

    @classmethod
    def create(cls, session, **kwargs):
        route_tag = cls(**kwargs) 
        session.add(route_tag) 
        session.flush()
        return route_tag
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, route_tag):
        try:
            route_tag = int(route_tag)
            return session.query(cls).filter_by(id=route_tag).first()
        except ValueError:
            print("Invalid route tag info ID.")
            return None

    @classmethod
    def delete_by_id(cls, session, route_tag_id):
        try:
            route_tag_id = int(route_tag_id)
        except ValueError:
            print("Invalid route tag info ID.")
            return False

        route_tag = session.query(cls).filter_by(id=route_tag_id).first()
        if not route_tag:
            return False

        session.delete(route_tag)
        return True