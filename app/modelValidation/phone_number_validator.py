# app.models.modelValidation.phone_number_validator.py

# used in validation classes

def phone_number_validator(phone, field="Phone Number"):
    if isinstance(phone, int):
        phone = str(phone)

    elif isinstance(phone, str):
        phone = phone.strip().replace("-", "").replace(" ", "")
    else:
        raise TypeError(f"{field} must be a string or integer")

    if not phone.isdigit():
        raise ValueError(f"{field} must contain only digits")

    if len(phone) != 10:
        raise ValueError(f"{field} must be exactly 10 digits long")

    return phone