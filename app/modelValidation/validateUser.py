# app/modelValidation/validateUser.py
#!/usr/bin/env python3
from app.models.user import ProfileType
class ValidateUser():
    all = []
    
    def __init__(self, real_name, username, email, phone_number, password, role, profile_type):
            self.real_name = real_name # Triggers the setter
            self.username = username
            self.email = email
            self.phone_number = phone_number
            self.password = password
            self.role = role
            self.profile_type = profile_type
            self.__class__.all.append(self)

    @property # by defining a property using the @property decorator, we access it like an attribute, not a method
    def real_name(self): # we can now access real_name as a property: instance.real_name other than instance.real_name()
        return self._real_name

    @real_name.setter
    def real_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Real name should be a string")
        
        try:
            first_name, last_name = name.strip().split() # unpack real name
        except ValueError:
             raise ValueError("Real name must include first and last name separated by a space")
        
        if not first_name or not last_name: # both names should be present
            raise ValueError("Real name must include both first and last name")
        self._real_name = name

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        if not isinstance(username, str):
            raise TypeError("Username should be a string")
        
        if not 3 <= len(username) <= 14:
            raise ValueError("Username must be between 3 and 15 characters long")
        
        if any(c.isupper() for c in username):
            raise ValueError("Username should only contain lowercase characters")
        
        if not any(c.isdigit() for c in username):
            raise ValueError("Username should contain at least one digit")
            
        self._username = username
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if email.count('@') != 1:
            raise ValueError("Email must contain exactly one '@' symbol.")
        
        local_part, domain_part = email.split('@')
        if not local_part or not domain_part:
            raise ValueError("Email must have both local and domain parts.")
        
        if '.' not in domain_part:
            raise ValueError("Email domain must contain a '.' (e.g. abc.com).")
        
        self._email = email
    
    
    @property
    def phone_number(self):
        return self._phone_number
    
    @phone_number.setter
    def phone_number(self, phone):
        if isinstance(phone, int):
            phone = str(phone)
        
        elif isinstance(phone, str):
            phone = phone.strip().replace("-", "").replace(" ", "") # Removing spaces, dashes, etc.
        else:
            raise TypeError("Phone number must be a string or integer")

        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits long")

        self._phone_number= phone
    
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        has_digit = False
        has_upper = False
        has_lower = False
        has_special = False

        for c in password:
            if c.isdigit():
                has_digit = True
            elif c.isupper():
                has_upper = True
            elif c.islower():
                has_lower = True
            elif not c.isalnum():
                has_special = True  # non-alphanumeric character

        if has_digit and has_upper and has_lower and has_special:
            self._password = password
        else:
            raise ValueError("Password must include uppercase, lowercase, digit, and special character.")


    @property
    def profile_type(self):
        return self._profile_type
    
    @profile_type.setter
    def profile_type(self, profile):
        if isinstance(profile, str):
            try:
                profile = ProfileType(profile.lower())  # Normalizing and converting string to Enum
            except ValueError:
                raise ValueError("Invalid profile type. Must be one of: customer, company, admin.")
        elif not isinstance(profile, ProfileType):
            raise TypeError("Profile type must be a string or ProfileType enum.")

        self._profile_type = profile


# Sample user validation =>
#     real_name="John Doe",
#     username="johnd2",
#     email="john@example.com",
#     phone_number="1234567890",
#     password="secure123!A",
#     role="user",
#     profile_type="customer"  # Can be a string or ProfileType.customer
