# app/modelValidation/validateService.py
#!/usr/bin/env python3
from .string_int_value_validator import string_int_value_validator

class ValidateService:
    def __init__(self, user_id, company_name, service_name, cost, license, image_url=None):
        self.user_id = self._validate_id(user_id, field="User ID")
        self.company_name = self._validate_nonempty_str(company_name, "Company Name")
        self.service_name = self._validate_nonempty_str(service_name, "Service Name")
        self.cost = self._validate_cost(cost)
        self.license = self._validate_nonempty_str(license, "License")
        self.image_url = self._validate_image_url(image_url)

    def _validate_id(self, val, field="User ID"):
        self._shipment_id = string_int_value_validator(val, field)

    def _validate_nonempty_str(self, val, field):
        if isinstance(val, str) and val.strip():
            return val.strip()
        raise ValueError(f"{field} cannot be empty.")

    def _validate_cost(self, val):
        self._shipment_id = string_int_value_validator(val, "Service cost")

    def _validate_image_url(self, url):
        if url is None or url.strip() == "":
            return None
        if isinstance(url, str) and url.startswith(("http://", "https://")):
            return url
        raise ValueError("Image URL must start with http:// or https://")

#     validate Test =>
#         user_id='12',
#         company_name='DropMate Ltd',
#         service_name='Express Shipping',
#         cost='200',
#         license='DML-009823',
#         image_url='https://example.com/logo.png'
