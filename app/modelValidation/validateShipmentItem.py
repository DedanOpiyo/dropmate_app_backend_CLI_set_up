# app/modelValidation/validateShipmentItem.py
from .string_int_value_validator import string_int_value_validator

class ValidateShipmentItem:
    def __init__(self, shipment_id, item_name, description, weight, quantity, value, category_id):
        self.shipment_id = shipment_id
        self.item_name = item_name
        self.description = description
        self.weight = weight
        self.quantity = quantity
        self.value = value
        self.category_id = category_id

    @property
    def shipment_id(self):
        return self._shipment_id

    @shipment_id.setter
    def shipment_id(self, val):
        self._shipment_id = string_int_value_validator(val, "Shipment ID")

    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, val):
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Item name must be a non-empty string.")
        self._item_name = val.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        if val is not None and not isinstance(val, str):
            raise ValueError("Description must be a string or None.")
        self._description = val.strip() if isinstance(val, str) else None

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, val):
        try:
            val = float(val)
        except (ValueError, TypeError):
            raise ValueError("Weight must be a number.")
        if val <= 0:
            raise ValueError("Weight must be greater than 0.")
        self._weight = val

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, val):
        self._quantity = string_int_value_validator(val, "Quantity")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = string_int_value_validator(val, "Value")

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, val):
        self._category_id = string_int_value_validator(val, "Category ID")


# try:
#     validated_item = ValidateShipmentItem(
#         shipment_id="5",
#         item_name="Laptop",
#         description="15-inch MacBook Pro",
#         weight="2.5",
#         quantity="2",
#         value="3000",
#         category_id="1"
#     )
#     print("Validated item:", vars(validated_item))
# except Exception as e:
#     print("Validation failed:", e)