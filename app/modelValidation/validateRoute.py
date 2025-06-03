# app/modelValidation/validateRoute.py
#!/usr/bin/env python3
from app.models.route import BorderTypeRt
from .string_int_value_validator import string_int_value_validator

class ValidateRoute:
    all = []

    def __init__(self, origin_location_id, destination_location_id, scope, route_group_id=None):
        self.origin_location_id = origin_location_id
        self.destination_location_id = destination_location_id
        self.route_group_id = route_group_id
        self.scope = scope
        self.__class__.all.append(self)

    @property
    def origin_location_id(self):
        return self._origin_location_id

    @origin_location_id.setter
    def origin_location_id(self, value):
        self._origin_location_id = string_int_value_validator(value, "origin_location_id")

    @property
    def destination_location_id(self):
        return self._destination_location_id

    @destination_location_id.setter
    def destination_location_id(self, value):
        self._destination_location_id = string_int_value_validator(value, "destination_location_id")

    @property
    def route_group_id(self):
        return self._route_group_id

    @route_group_id.setter
    def route_group_id(self, value):
        self._route_group_id = string_int_value_validator(value, "route_group_id")

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, value):
        if isinstance(value, str):
            try:
                self._scope = BorderTypeRt(value.lower()) # intra_city, inter_city, inter_county, trans_county, cross_country
            except ValueError:
                raise ValueError(f"Invalid scope: '{value}'. Must be one of: {', '.join([s.value for s in BorderTypeRt])}") # joining acceptable enumerations - from dict-like to list
        elif isinstance(value, BorderTypeRt):
            self._scope = value
        else:
            raise TypeError("Scope must be a string or BorderTypeRt enum")

# try:
#     validated = validateShipment(
#         origin_location_id='12',
#         destination_location_id='24',
#         scope='intra_city',
#         route_group_id='person'
#     )
#     print("Service validated:", vars(validated))
# except Exception as e:
#     print("Validation error:", e)   