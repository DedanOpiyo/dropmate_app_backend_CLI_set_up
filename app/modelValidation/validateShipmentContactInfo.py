# app/modelValidation/validateShipmentContactInfo.py

from .string_int_value_validator import string_int_value_validator
from .phone_number_validator import phone_number_validator

class ValidateShipmentContactInfo:
    def __init__(self, shipment_id, sender_name, sender_phone, sender_address,
                 receiver_name, receiver_phone, receiver_address, info_provider_id):
        
        self.shipment_id = shipment_id
        self.sender_name = sender_name
        self.sender_phone = sender_phone
        self.sender_address = sender_address
        self.receiver_name = receiver_name
        self.receiver_phone = receiver_phone
        self.receiver_address = receiver_address
        self.info_provider_id = info_provider_id

    @property
    def shipment_id(self):
        return self._shipment_id

    @shipment_id.setter
    def shipment_id(self, value):
        self._shipment_id = string_int_value_validator(value, "Shipment ID")

    @property
    def sender_name(self):
        return self._sender_name

    @sender_name.setter
    def sender_name(self, value):
        self._sender_name = self._validate_nonempty_str(value, "Sender Name")

    @property
    def sender_phone(self):
        return self._sender_phone

    @sender_phone.setter
    def sender_phone(self, value):
        self._sender_phone = phone_number_validator(value, "Sender Phone")

    @property
    def sender_address(self):
        return self._sender_address

    @sender_address.setter
    def sender_address(self, value):
        self._sender_address = self._validate_nonempty_str(value, "Sender Address")

    @property
    def receiver_name(self):
        return self._receiver_name

    @receiver_name.setter
    def receiver_name(self, value):
        self._receiver_name = self._validate_nonempty_str(value, "Receiver Name")

    @property
    def receiver_phone(self):
        return self._receiver_phone

    @receiver_phone.setter
    def receiver_phone(self, value):
        self._receiver_phone = phone_number_validator(value, "Receiver Phone")

    @property
    def receiver_address(self):
        return self._receiver_address

    @receiver_address.setter
    def receiver_address(self, value):
        self._receiver_address = self._validate_nonempty_str(value, "Receiver Address")

    @property
    def info_provider_id(self):
        return self._info_provider_id

    @info_provider_id.setter
    def info_provider_id(self, value):
        self._info_provider_id = string_int_value_validator(value, "Info Provider ID")

    def _validate_nonempty_str(self, value, field):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string.")
        return value.strip()