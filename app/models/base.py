# app/models/models.py
import enum

from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# convention dictionary for consistent naming in db constraints(e.g FKs)
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Import all models to register them centrally
from app.models.shipment import Shipment
from app.models.user import User
from app.models.location import Location
from app.models.route import Route
from app.models.route_location import RouteLocation
from app.models.service import Service
from app.models.shippingCost import ShippingCost
from app.models.route_group import RouteGroup
from app.models.shipmentItem import ShipmentItem
from app.models.routeTag import RouteTag
from app.models.ItemCategory import ItemCategory
from app.models.drop_log import DropLog
from app.models.border import Border
from app.models.shipmentContactInfo import ShipmentContactInfo


# from .user import User
# from .shipment import Shipment
# from .location import Location
# from .route import Route
# from .route_location import RouteLocation
# from .service import Service
# from .shippingCost import ShippingCost
# from .route_group import RouteGroup
# from .shipmentItem import ShipmentItem
# from .routeTag import RouteTag
# from .ItemCategory import ItemCategory
# from .drop_log import DropLog
# from .border import Border
