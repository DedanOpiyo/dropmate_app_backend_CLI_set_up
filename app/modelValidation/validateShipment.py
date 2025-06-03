# app/modelValidation/validateShipment.py
#!/usr/bin/env python3
from app.models.shipment import ShipmentStatus, ShipmentType
from .string_int_value_validator import string_int_value_validator

class ValidateShipment:
    all = []

    def __init__(self, user_id, origin_location_id, destination_location_id, route_id, service_id, status, shipment_type, shipping_cost):
        self.user_id = user_id
        self.origin_location_id = origin_location_id
        self.destination_location_id = destination_location_id
        self.route_id = route_id
        self.service_id = service_id
        self.status = status
        self.shipment_type = shipment_type
        self.shipping_cost = shipping_cost
        self.__class__.all.append(self)

    @classmethod
    def _convert_to_positive_int(cls, value, field_name):  # reusable func to validate string id's/costs if any
        return string_int_value_validator(value, field_name)

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = self._convert_to_positive_int(value, "user_id")

    @property
    def origin_location_id(self):
        return self._origin_location_id

    @origin_location_id.setter
    def origin_location_id(self, value):
        self._origin_location_id = self._convert_to_positive_int(value, "origin_location_id")

    @property
    def destination_location_id(self):
        return self._destination_location_id

    @destination_location_id.setter
    def destination_location_id(self, value):
        self._destination_location_id = self._convert_to_positive_int(value, "destination_location_id")

    @property
    def route_id(self):
        return self._route_id

    @route_id.setter
    def route_id(self, value):
        self._route_id = self._convert_to_positive_int(value, "route_id")

    @property
    def service_id(self):
        return self._service_id

    @service_id.setter
    def service_id(self, value):
        self._service_id = self._convert_to_positive_int(value, "service_id")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, str):
            try:
                self._status = ShipmentStatus(value.lower())
            except ValueError:
                raise ValueError(f"Invalid status: '{value}'. Must be one of: {', '.join([s.value for s in ShipmentStatus])}") # joining acceptable enumerations - from dict-like to list
        elif isinstance(value, ShipmentStatus):
            self._status = value
        else:
            raise TypeError("Status must be a string or ShipmentStatus enum")

    @property
    def shipment_type(self):
        return self._shipment_type

    @shipment_type.setter
    def shipment_type(self, value):
        if isinstance(value, str):
            try:
                self._shipment_type = ShipmentType(value.lower())
            except ValueError:
                raise ValueError(f"Invalid shipment_type: '{value}'. Must be one of: {', '.join([t.value for t in ShipmentType])}")
        elif isinstance(value, ShipmentType):
            self._shipment_type = value
        else:
            raise TypeError("shipment_type must be a string or ShipmentType enum")

    @property
    def shipping_cost(self):
        return self._shipping_cost

    @shipping_cost.setter
    def shipping_cost(self, value):
        if isinstance(value, (int, float)):
            if value <= 0:
                raise ValueError("Shipping cost must be greater than 0")
            self._shipping_cost = value
        elif isinstance(value, str):
            if value.strip().isdigit():
                numeric_value = int(value.strip())
                if numeric_value <= 0:
                    raise ValueError("Shipping cost must be greater than 0")
                self._shipping_cost = numeric_value
            else:
                raise TypeError("Shipping cost string must contain only digits")
        else:
            raise TypeError("Shipping cost must be a number or digit string")

##
# def test_validate_shipment_with_string_ids():
#     try:
#         shipment = validateShipment(
#             user_id='5',
#             origin_location_id='10',
#             destination_location_id='20',
#             route_id='30',
#             service_id='40',
#             status='in transit',
#             shipment_type='person',
#             shipping_cost='150'
#         )
#         print("PASS: Validation with string IDs succeeded.")
#         print(vars(shipment))
#     except Exception as e:
#         print("FAIL:", e)

# testr = test_validate_shipment_with_string_ids()
# print(testr)