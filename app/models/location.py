# app/models/location.py
# from app.models.base import Base
from .base import Base  # relative import
import enum

from sqlalchemy import func, Enum
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.orm import relationship

class LocationType(enum.Enum):
    estate = "estate"
    village = "village"
    town = "town"
    city = "city"
    county = "county"
    country = "country"
    port = "port"
    hub = "hub"
    special_zone = "special_zone"

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) # e.g. Karen, Mombasa, Serengeti
    type = Column(Enum(LocationType), nullable=False)  # e.g. city, county, country
    # Self-referencing hierarchy
    parent_id = Column(Integer, ForeignKey('locations.id'), nullable=True) # hierarchical location parent i.e : estate -> town -> county -> country
    country_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    
    constituency = Column(String(), nullable=False) # e.g. Westlands, Embakassi (optional political/administrative unit)
    description = Column(Text) # nearby parks, hotels, game reserves, etc.
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True) # optional geolocation
    is_border = Column(Boolean, default=False) # is it a border or not
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())


    # relationships
    shipments_originating = relationship('Shipment', back_populates='origin', foreign_keys='Shipment.origin_location_id') # we could do the same for destination
    shipments_arriving = relationship('Shipment', foreign_keys='Shipment.destination_location_id', back_populates='destination')
    
    routes_originating = relationship('Route', back_populates='origin', foreign_keys='Route.origin_location_id')
    routes_ending = relationship('Route', back_populates='destination', foreign_keys='Route.destination_location_id')

    route_locations = relationship('RouteLocation', back_populates='location')  # for many-to-many with Route

    # self-referential relationships # one-to-one
    parent = relationship("Location", foreign_keys=[parent_id], remote_side=[id], back_populates="children")
    children = relationship("Location", back_populates="parent", foreign_keys=[parent_id]) 
    # Country reference (separated from parent/child)
    # country = relationship("Location", foreign_keys=[country_id], backref="contained_locations")
    country = relationship("Location", foreign_keys=[country_id], back_populates="contained_locations", remote_side=[id]) # Location belongs to one country
    contained_locations = relationship("Location", back_populates="country", foreign_keys=[country_id]) # Country has many contained locations
    
    border_info = relationship("Border", back_populates="location", uselist=False)  # one-to-one

    # Optional # anchoring location for RouteGroups
    route_groups = relationship("RouteGroup", back_populates="region_location")

    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, location_id):
        try:
            location_id = int(location_id)
            return session.query(cls).filter_by(id=location_id).first()
        except ValueError:
            print("Invalid location ID.")
            return None

    @classmethod
    def create(cls, session, **kwargs):
        location = cls(**kwargs)
        session.add(location)
        session.flush()
        return location

    @classmethod
    def delete_by_id(cls, session, location_id):
        location = cls.find_by_id(session, location_id)
        if not location:
            return False
        session.delete(location)
        return True











# when is_border is True/changed to True, CLI should allow user to seed Border model

# ##
# # Get all top-level locations
# top_level = session.query(Location).filter(Location.parent_id == None).all()

# # Drill down from a location
# def get_location_hierarchy(location):
#     hierarchy = [location]
#     while location.parent:
#         hierarchy.append(location.parent)
#         location = location.parent
#     return list(reversed(hierarchy))  # country -> city -> estate

# ----

# shipments — borders inferred via route_locations
# To get all borders involved in a shipment, use:
# SELECT l.*
# FROM route_locations rl
# JOIN locations l ON rl.location_id = l.id
# WHERE rl.route_id = :route_id AND l.is_border = true;

# here: Shipment links to route, derives border crossings from route locations.


# Display full hierarchy of a location: recursive query on parent_id || You can use recursive queries on locations.parent_id to trace full hierarchies.
# Trace if a shipment crosses a border: match shipment route locations with is_border = true
