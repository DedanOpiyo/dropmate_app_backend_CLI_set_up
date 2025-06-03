# Import all models to register them centrally
# app/models/__init__.py

from .base import Base  # Declarative base with naming convention

from .user import User
from .shipment import Shipment
from .location import Location
from .route import Route
from .route_location import RouteLocation
from .service import Service
from .shippingCost import ShippingCost
from .route_group import RouteGroup
from .shipmentItem import ShipmentItem
from .routeTag import RouteTag
from .ItemCategory import ItemCategory
from .drop_log import DropLog
from .border import Border
from .shipmentContactInfo import ShipmentContactInfo
