# app/modelValidation/validateItemCategory.py

class ValidateItemCategory:
    def __init__(self, name, base_rate=None, description=None):
        self.name = self.validate_name(name)
        self.base_rate = self.validate_base_rate(base_rate)
        self.description = description.strip() if description else None

    def validate_name(self, name):
        if not name or not name.strip():
            raise ValueError("Item category name is required.")
        return name.strip()

    def validate_base_rate(self, rate):
        if rate is None or rate == "":
            return 1.0
        try:
            rate = float(rate)
            if rate <= 0:
                raise ValueError("Base rate must be positive.")
            return rate
        except ValueError:
            raise ValueError("Base rate must be a valid number.")
