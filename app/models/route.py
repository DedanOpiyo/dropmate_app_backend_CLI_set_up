# app/models/route.py
from .base import Base  # relative import
import enum

from sqlalchemy import func, Enum
from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import relationship

class BorderTypeRt(enum.Enum): # similar to borders table
    intra_city = "intra_city"
    inter_city = "inter_city"
    inter_county = "trans_county"
    trans_county = "trans_county"
    cross_country = "cross_country"

class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    origin_location_id = Column(Integer, ForeignKey('locations.id'))
    destination_location_id = Column(Integer, ForeignKey('locations.id'))
    route_group_id = Column(Integer, ForeignKey('route_groups.id'), nullable=True) # grouping by scope (e.g., all within Nairobi)
    scope = Column(Enum(BorderTypeRt))  # intra_city, inter_city, inter_county, trans_county, cross_country (similar to border_type)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    origin = relationship("Location", foreign_keys=[origin_location_id], back_populates="routes_originating")
    destination = relationship("Location", foreign_keys=[destination_location_id], back_populates="routes_ending")
    shipments = relationship("Shipment", back_populates="route")
    route_group = relationship("RouteGroup", back_populates="routes")  # Each Route has one optional route_group_id. Each RouteGroup has many Routes (one-to-many). # optional
    route_locations = relationship("RouteLocation", back_populates="route", order_by="RouteLocation.sequence") # RouteLocation - intermediate points (bridge table)

    shipping_cost = relationship("ShippingCost", uselist=False, back_populates="route") # one-to-one
    tags = relationship('RouteTag', back_populates='route')

    @classmethod
    def create(cls, session, **kwargs):
        route = cls(**kwargs) 
        session.add(route) 
        session.flush()
        return route
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, keyword):
        return session.query(cls).filter(
            cls.id == keyword
        ).first()

    @classmethod
    def delete_by_id(cls, session, route_id):
        try:
            route_id = int(route_id)
        except ValueError:
            print("Invalid route tag info ID.")
            return False

        route = session.query(cls).filter_by(id=route_id).first()
        if not route:
            return False

        session.delete(route)
        return True

    def __repr__(self):
        return (f"Route: id={self.id}"
            f"origin_location_id={self.origin_location_id}"
            f"destination_location_id={self.destination_location_id}"
            f"shipping_cost={self.shipping_cost}"
            f"route_group_id={self.route_group_id}"
            f"scope={self.scope}"
            f"created_at={self.created_at}"
            f"updated_at={self.updated_at}")
