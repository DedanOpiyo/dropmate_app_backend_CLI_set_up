from datetime import datetime
from .string_int_value_validator import string_int_value_validator

class ValidateShippingCost:
    def __init__(self, route_id, cost_value, start_date=None, end_date=None, active=True):
        self.route_id = route_id
        self.cost_value = cost_value
        self.start_date = start_date
        self.end_date = end_date
        self.active = active

    @property
    def route_id(self):
        return self._route_id

    @route_id.setter
    def route_id(self, val):
        self._route_id = string_int_value_validator(val, "Route ID")

    @property
    def cost_value(self):
        return self._cost_value

    @cost_value.setter
    def cost_value(self, val):
        self._cost_value = string_int_value_validator(val, "Cost Value")

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, val):
        self._start_date = self._validate_date(val, "Start Date")

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, val):
        self._end_date = self._validate_date(val, "End Date")

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val):
        if not isinstance(val, bool):
            raise ValueError("Active must be a boolean.")
        self._active = val

    def _validate_date(self, val, field_name):
        if val is None or val == "":
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"{field_name} must be in YYYY-MM-DD format.")
