# app.models.modelValidation.string_int_value_validator.py

# used in validation classes

def string_int_value_validator(value, field_name): # reusable func to validate string id's/costs if any
    if isinstance(value, int):
        if value <= 0:
            raise ValueError(f"{field_name} must be a positive integer")
        return value
    elif isinstance(value, str):
        if value.strip().isdigit():
            int_val = int(value.strip())
            if int_val <= 0:
                raise ValueError(f"{field_name} must be a positive integer")
            return int_val
        else:
            raise TypeError(f"{field_name} must be an integer or digit-only string")
    else:
        raise TypeError(f"{field_name} must be an integer or string")
    