# Dropmate App Backend Implementation using SQLAlchemy

## Project Goals

- Use SQLAlchemy to join tables with one-to-one, one-to-many, and many-to-many
  relationships.

---

## Contact Information
For questions, suggestions, or contributions, feel free to reach out:

- Developer: [Dedan Opiyo]

- Email: [dedandedan2@gmail.com]

- GitHub: https://github.com/DedanOpiyo?tab=repositories


## Introduction

The Dropment app models a rich set of relationships between inter-connected tables, showcasing the advanced features and flexibility of SQLAlchemy's ORM.

This project demonstrates key relational patterns, including **one-to-one**, **one-to-many**, and **many-to-many** associations across different models. 

For example, a single user can place multiple shipments or orders, which necessitates a `User` model and a related `shipments` table. The `shipments` table, in turn, connects to other entities such as `locations`, and more.  
__Explore the complete schema:__  
[Entity Relationship Diagram(ERD)](https://dbdiagram.io/d/683419abb9f7446da323900c).

### Relationship strategy

While SQLAlchemy offers both `backref()` and `back_populates` for setting up bidirectional relationships, this project primarily uses `back_populates` due to its explicitness and flexibility—ideal for evolving and complex schemas.  

Only **one use of** `backref()` exists in the project: the **one-to-many** relationship between `User` and `Shipment`. In this case, `backref()` is defined on the **"one" side** (`User`), which automatically sets up access to the related `User` from the `Shipment` model.  
Since `backref()` only needs to be defined on **one side**, the Shipment model does not explicitly define a reciprocal relationship—this is intentional and should not cause confusion.

---

## Project Setup  

Fork and clone the repo or follow the steps below to set up the Dropment backend environment.  
**1. Initialize Project Structure**  

```bash
mkdir dropmate_app_backend_improvement
cd dropmate_app_backend_improvement
pipenv install
pipenv shell
touch README.md
touch .gitignore
mkdir app
cd app
touch models.py
touch debug.py
touch seed.py
touch db.py
```
**2. Pipfile Packages**  

Inside your Pipfile, add the following under [packages]:  

``` bash
[packages]
alembic = "*"
ipdb = "*"
sqlalchemy = "1.4.42"
faker = "*"
choice = "*"
```

**3. Install Dependencies**   

From the project root:  
``` bash
pipenv install
```
Enter the virtual environment: run `pipenv shell`

**4. Initialize Alembic (Inside app/)**  

``` bash
cd app
alembic init migrations
```

**5. Create Your Models (app/models.py)**  

``` bash
from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Convention dictionary for consistent naming (e.g., foreign keys)
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

```

**6. Link Alembic to Your Models**
Edit app/env.py and add:  

find `target_metadata = None` normally in line 21. Then point the metadata as follows:

``` bash
from models import Base
target_metadata = Base.metadata
```

Because we will be modularizing the models (i.e. spliting them across multiple files like user.py, shipment.py, etc.),
we will have to make sure Alembic "sees" our models by explicitly importing them before registering our metadata: `target_metadata = Base.metadata`.  
Since we are not defining the models in `models.py` alembic does not detect them. We'll import them as so:   
``` bash
import sys
import os

# Make sure app is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Base (automatically imports all models)
from app.models.base import Base # Importing Base from the central definition

target_metadata = Base.metadata # Metadata registration # point target_metadata = accordingly
```

We will import the models we want to migrate then run `Alembic --autogenerate ...`.   
For now, lets exclude model importation since we do not have any models to migrate yet.

**7. Configure Database URL**
Update the sqlalchemy.url in alembic.ini:  

find `sqlalchemy.url = driver://user:pass@localhost/dbname` normally in line 87. Then point the database as follows:

``` bash
sqlalchemy.url = sqlite:///app/dropmate.db

```

**8. Run Alembic Commands (Inside app/)**
Make sure you're in the directory with alembic.ini:  

``` bash
cd app
alembic revision --autogenerate -m "create db"
alembic upgrade head

```

### Project Structure

You can run `tree` in your terminal to view the file layout. As the project evolves, each model will be defined in its **own file** for better modularity and clarity.  
Below is the current structure, which includes `user.py`, `shipment.py`, `location.py` and other modek files—all separated out from the central `models.py`. You’ll see how these are integrated as the project unfolds.  
```bash
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── app
│   ├──  __init__.py
│   ├── __pycache__
│   │   ├── cli.cpython-312.pyc
│   │   ├── db.cpython-312.pyc
│   │   ├── helpers.cpython-312.pyc
│   │   └── seed.cpython-312.pyc
│   ├── alembic.ini
│   ├── cli.py
│   ├── db.py
│   ├── debug.py
│   ├── dropmate.db
│   ├── helpers.py
│   ├── menus
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── dev_tools_menu.cpython-312.pyc
│   │   │   ├── estimate_shipping_cost_menu.cpython-312.pyc
│   │   │   ├── item_category_menu.cpython-312.pyc
│   │   │   ├── location_menu.cpython-312.pyc
│   │   │   ├── manage_shipments.cpython-312.pyc
│   │   │   ├── route_menu.cpython-312.pyc
│   │   │   ├── sender_receiver_menu.cpython-312.pyc
│   │   │   ├── shipment_item_menu.cpython-312.pyc
│   │   │   ├── shipment_menu.cpython-312.pyc
│   │   │   ├── shipping_cost_menu.cpython-312.pyc
│   │   │   └── user_menu.cpython-312.pyc
│   │   ├── dev_tools_menu.py
│   │   ├── estimate_shipping_cost_menu.py
│   │   ├── item_category_menu.py
│   │   ├── location_menu.py
│   │   ├── manage_shipments.py
│   │   ├── route_location.py
│   │   ├── route_menu.py
│   │   ├── sender_receiver_menu.py
│   │   ├── shipment_item_menu.py
│   │   ├── shipment_menu.py
│   │   ├── shipping_cost_menu.py
│   │   └── user_menu.py
│   ├── migrations
│   │   ├── README
│   │   ├── __pycache__
│   │   │   └── env.cpython-312.pyc
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── 458a23cb9aca_create_db.py
│   │       ├── 963ffa3c9692_create_db.py
│   │       └── __pycache__
│   │           ├── 458a23cb9aca_create_db.cpython-312.pyc
│   │           └── 963ffa3c9692_create_db.cpython-312.pyc
│   ├── modelValidation
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── phone_number_validator.cpython-312.pyc
│   │   │   ├── string_int_value_validator.cpython-312.pyc
│   │   │   ├── validateItemCategory.cpython-312.pyc
│   │   │   ├── validateRoute.cpython-312.pyc
│   │   │   ├── validateShipment.cpython-312.pyc
│   │   │   ├── validateShipmentContactInfo.cpython-312.pyc
│   │   │   ├── validateShipmentItem.cpython-312.pyc
│   │   │   ├── validateShippingCost.cpython-312.pyc
│   │   │   └── validateUser.cpython-312.pyc
│   │   ├── phone_number_validator.py
│   │   ├── string_int_value_validator.py
│   │   ├── validateItemCategory.py
│   │   ├── validateRoute.py
│   │   ├── validateService.py
│   │   ├── validateShipment.py
│   │   ├── validateShipmentContactInfo.py
│   │   ├── validateShipmentItem.py
│   │   ├── validateShippingCost.py
│   │   └── validateUser.py
│   ├── models
│   │   ├── ItemCategory.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── ItemCategory.cpython-312.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── base.cpython-312.pyc
│   │   │   ├── border.cpython-312.pyc
│   │   │   ├── drop_log.cpython-312.pyc
│   │   │   ├── location.cpython-312.pyc
│   │   │   ├── route.cpython-312.pyc
│   │   │   ├── routeTag.cpython-312.pyc
│   │   │   ├── route_group.cpython-312.pyc
│   │   │   ├── route_location.cpython-312.pyc
│   │   │   ├── service.cpython-312.pyc
│   │   │   ├── shipment.cpython-312.pyc
│   │   │   ├── shipmentContactInfo.cpython-312.pyc
│   │   │   ├── shipmentItem.cpython-312.pyc
│   │   │   ├── shippingCost.cpython-312.pyc
│   │   │   └── user.cpython-312.pyc
│   │   ├── base.py
│   │   ├── border.py
│   │   ├── drop_log.py
│   │   ├── location.py
│   │   ├── route.py
│   │   ├── routeTag.py
│   │   ├── route_group.py
│   │   ├── route_location.py
│   │   ├── service.py
│   │   ├── shipment.py
│   │   ├── shipmentContactInfo.py
│   │   ├── shipmentItem.py
│   │   ├── shippingCost.py
│   │   └── user.py
│   ├── seed.py
│   └── test_log.py
└── logs
    └── dev.log
```
#### Defining Models in Separate Files  

It’s recommended to define each model (e.g., `User`, `Shipment`, `Location`) in its own file instead of cluttering `models.py`.  
To do this, each model file should:
-Import `Base` from `models.py`
-**Import SQLAlchemy components** required for table definitions and relationships  

Here’s the standard import pattern for a model file:  
```bash
from models import Base

from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref

```
---

## Implementations

With the project setup out of the way, let's dive into the actual implementation.    
We’ll start by defining three core models: `User`, `Shipment`, and `Location`, followed by running an Alembic migration:  
```bash
# From project root (dropmate_app_backend_improvement/):

PYTHONPATH=. alembic -c app/alembic.ini revision --autogenerate -m "create db"
```  
We're using **table names** (not class names) in the migration commit message for clarity.
We'll choose to either migrate the models **individually** or in groups of **two or three**.
After each revision command, we'll apply the changes using:
```bash
PYTHONPATH=. alembic -c app/alembic.ini upgrade head
``` 

### user.py

According to our [Entity Relationship Diagram(ERD)](https://dbdiagram.io/d/683419abb9f7446da323900c), a `User` can have/place multiple orders/shipments (one-to-many relationship).  
To represent this, we define a relationship to the `Shipment` model.  
To do that, we'll first need to create the `shipment.py `file and define the `Shipment` model, as a `User` is linked to it via the `user_id` foreign key.  
- The column `user_id` in the `shipments` table references `users.id`.
- We're using `backref()` to automatically create the reverse relationship from `Shipment` back to `User`.  

```bash
shipment.py  

user = relationship('User', backref='shipments') 
```  

```bash  
# app/models/user.py
from .base import Base  # relative import 
import enum

from sqlalchemy import func, Enum
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class ProfileType(enum.Enum):
    customer = 'customer'
    company = 'company'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    real_name = Column(String())
    username = Column(String())
    email = Column(String(), unique=True)
    phone_number = Column(Integer())
    password = Column(String())
    role = Column(String(), nullable=True) 
    profile_type = Column(Enum(ProfileType), default=ProfileType.customer) 
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Relationships *Shipment moved
    services = relationship('Service', back_populates='user') # One-to-many relationship with Service
    provided_contact_infos = relationship("ShipmentContactInfo", back_populates="info_provider")

    # SQLAlchemy automatically provides a default constructor that accepts keyword arguments matching our model's attributes (columns and relationships). We'll exclude optional overriding __init__
    @classmethod
    def create(cls, session, **kwargs):
        user = cls(**kwargs) # no need for custom __init__
        session.add(user) # no session.commit(), context manager in lib will do that for us
        session.flush() # forcing sql insertion to get id
        return user

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_username_or_email(cls, session, keyword):
        return session.query(cls).filter(
            (cls.username == keyword) | (cls.email == keyword)
        ).first()

    @classmethod
    def delete_by_username(cls, session, username):
        user = session.query(cls).filter_by(username=username).first()
        if user:
            session.delete(user)
            return True
        return False
    
    def __repr__(self):
        return (f"User: id={self.id}" 
            f"Real_name={self.real_name}" 
            f"Username={self.username}" 
            f"Email={self.email}" 
            f"Phone_number={self.phone_number}" 
            f"Role={self.role}" 
            f"Profile_type={self.profile_type}")
```

With this setup:
- We can access a user's shipments through the shipments attribute by querying the User model: `session.query(User).first().shipments`
- We can access the user from a shipment through the 'backref-user': `shipment.user`

As at now we are not able to complete the query yet because we have not filled/seeded our database/tables.
You'll see how this works more clearly after we do so through the seed.py file.

From the ERD you can also notice that `User` has a relationship with `Service`.
A user can add a service or services. This is a `one-to-many relationship` too, but instead of using `backref()` we'll use `back_populates` in both tables:
```bash
# user.py  

services = relationship('Service', back_populates='user')  
```  
When we create service.py we will have to add:  
```bash
# service.py  

user = relationship('User', back_populates='services')  
```  
and a linking attribute to the `Service` class/model: `user_id = Column(Integer(), ForeignKey('users.id))`

### shipment.py

Here's the definition of the `Shipment` model, which links to `User`, `Location`, `Route`, `Service`, and other related entities:

```bash
from models import Base
from enum import Enum as PyEnum

from sqlalchemy import func, Enum
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref

class ShipmentStatus(PyEnum):
    pending = "pending"
    in_transit = "in transit"
    delivered = "delivered"

class ShipmentType(PyEnum):
    goods = "goods"
    person = "person"

class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id')) # no relationship needed here, `backref()` was used in user.py(`User` model)
    origin_location_id = Column(Integer, ForeignKey('locations.id')) # Many-to-one relationship. Many shipments can originate from one location
    destination_location_id = Column(Integer(), ForeignKey('locations.id'))
    route_id = Column(Integer, ForeignKey('routes.id'))
    service_id = Column(Integer(), ForeignKey('services.id'))
    status = Column(Enum(ShipmentStatus), nullable=False, default=ShipmentStatus.pending)  # pending, in transit, delivered
    shipment_type = Column(Enum(ShipmentType), default=ShipmentType.goods) # goods, person
    shipping_cost = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Relationships
    service = relationship('Service', back_populates="shipments") # one-to-many
    origin = relationship('Location', foreign_keys=[origin_location_id], back_populates='shipments_originating') # disambiguate the FK column in the relationship since there are multiple FKs to the same table - Location.
    destination = relationship('Location', foreign_keys=[destination_location_id], back_populates='shipments_arriving')
    route = relationship('Route', back_populates='shipments') # Many-to-one. One Shipment uses one Route. One Route can be used by many Shipments
    shipment_items = relationship('ShipmentItem', back_populates='shipment') 
    drop_logs = relationship('DropLog', back_populates='shipment')
```

> Note: Although we’re using `backref` in the `User` model, **we are not redefining the same relationship with** `back_populates` in `Shipment`.

#### Essence of enumeration in the model:
We are using Python’s `Enum` from the `enum` module, imported as `PyEnum`, to avoid naming conflicts with SQLAlchemy’s `Enum`. In other classes, you may see `enum.Enum` used directly—this is intentional and should not cause confusion.

Enumerations are used here to clearly define and restrict expected input values, ensuring consistency across the application. They also offer compatibility with various databases and help enforce a standardized structure.

Additionally, we’ve specified default values for these enumerations where applicable, to clarify expected behavior and reduce the risk of unexpected states.

#### Essence of foreign_keys in defining relationships the model:
In this model, we use the `foreign_keys` argument to clearly define relationships when multiple fields reference the same parent table (`Location`). Specifically, both `origin_location_id` and `destination_location_id` point to `locations.id`:
```bash
origin_location_id = Column(Integer, ForeignKey('locations.id'))
destination_location_id = Column(Integer, ForeignKey('locations.id'))  
```  

```bash
origin = relationship('Location', foreign_keys=[origin_location_id], back_populates='shipments_originating')
destination = relationship('Location', foreign_keys=[destination_location_id], back_populates='shipments_arriving')
```  

Without this explicit declaration, SQLAlchemy could get confused about which column to use when joining. By specifying foreign_keys, we ensure that:

- origin retrieves shipments departing from a location
- destination retrieves shipments arriving at a location

in Location model, we also define the reciprocal relationship:
```bash
shipments_originating = relationship('Shipment', back_populates='origin', foreign_keys='Shipment.origin_location_id')
shipments_arriving = relationship('Shipment', foreign_keys='Shipment.destination_location_id', back_populates='destination')  
```  

This disambiguation will allow SQLAlchemy to map relationships accurately and maintain clarity in the data model.
> We'll be using this pattern in any instance where multiple columns in a model reference the same attribute (typically the primary key) of another model.

### location.py

```py
# location.py

from models import Base
import enum

from sqlalchemy import func, Enum
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.orm import relationship

class LocationType(enum.Enum):
    estate = "estate"
    village = "village"
    town = "town"
    city = "city"
    county = "county"
    country = "country"
    port = "port"
    hub = "hub"
    special_zone = "special_zone"

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) # e.g. Karen, Mombasa, Serengeti
    type = Column(Enum(LocationType), nullable=False)  # e.g. city, county, country
    # Self-referencing hierarchy
    parent_id = Column(Integer, ForeignKey('locations.id'), nullable=True) # hierarchical location parent i.e : estate -> town -> county -> country
    country_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    
    constituency = Column(String(), nullable=False) # e.g. Westlands, Embakassi (optional political/administrative unit)
    description = Column(Text) # nearby parks, hotels, game reserves, etc.
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True) # optional geolocation
    is_border = Column(Boolean, default=False) # is it a border or not
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())


    # relationships
    shipments_originating = relationship('Shipment', back_populates='origin', foreign_keys='Shipment.origin_location_id') # we could do the same for destination
    shipments_arriving = relationship('Shipment', foreign_keys='Shipment.destination_location_id', back_populates='destination')
    
    routes_originating = relationship('Route', back_populates='origin', foreign_keys='Route.origin_location_id')
    routes_ending = relationship('Route', back_populates='destination', foreign_keys='Route.destination_location_id')

    route_locations = relationship('RouteLocation', back_populates='location')  # for many-to-many with Route

    # self-referential relationships # one-to-one
    parent = relationship("Location", foreign_keys=[parent_id], remote_side=[id], back_populates="children")
    children = relationship("Location", back_populates="parent", foreign_keys=[parent_id]) 

    country = relationship("Location", foreign_keys=[country_id], back_populates="contained_locations")
    contained_locations = relationship("Location", back_populates="country", foreign_keys=[country_id])
    
    border_info = relationship("Border", back_populates="location", uselist=False)  # one-to-one

    # Optional # anchoring location for RouteGroups
    route_groups = relationship("RouteGroup", back_populates="region_location")

    # __repr__()

```

Following our important rule:
Whenever we have multiple foreign keys to the same table, and we're using relationship(), we should always specify:

- `foreign_keys=[...]` — to remove ambiguity

- `remote_side=[id]` — only for self-referencing relationships  

**Notice:**
```py
parent = relationship("Location", foreign_keys=[parent_id], remote_side=[id], back_populates="children")
```
With `foreign_keys=[parent_id]` SQLAlchemy knows we're using parent_id (not country_id) for the parent/children hierarchy.  
This is because `parent_id` and `country_id` attributes are self referencing: both references the `locations.id` (in the same table -locations)

```py
country = relationship("Location", foreign_keys=[country_id], back_populates="contained_locations", remote_side=[id])
contained_locations = relationship("Location", foreign_keys=[country_id], back_populates="country")   
```  
**Explaining the Self-References with a table**
`Locations table:`

| id | name             | type    | parent\_id | country\_id | constituency | description         |
| -- | ---------------- | ------- | ---------- | ----------- | ------------ | ------------------- |
| 1  | Kenya            | country | `NULL`     | `NULL`      | N/A          | The country itself  |
| 2  | Nairobi County   | county  | NULL       | 1           | N/A          | A county in Kenya   |
| 3  | Westlands        | town    | 2          | 1           | Westlands    | A town in Nairobi   |
| 4  | Brookside Estate | estate  | 3          | 1           | Westlands    | Estate in Westlands |

Looking at the table:  
 
- `parent_id:` forms a hierarchical tree (e.g., estate -> town -> county).

- `country_id:` always points to the top-level country, will be useful for filtering or joining (by national borders for example).  


### route.py

```py
# route.py

# app/models/route.py
# from app.models.base import Base
from .base import Base  # relative import
import enum

from sqlalchemy import func, Enum
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class BorderTypeRt(enum.Enum):
    intra_city = "intra_city"
    inter_city = "inter_city"
    inter_county = "trans_county"
    trans_county = "trans_county"
    cross_country = "cross_country"

class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    origin_location_id = Column(Integer, ForeignKey('locations.id'))
    destination_location_id = Column(Integer, ForeignKey('locations.id'))
    route_group_id = Column(Integer, ForeignKey('route_groups.id'), nullable=True) # grouping by scope (e.g., all within Nairobi)
    scope = Column(Enum(BorderTypeRt))  # intra_city, inter_city, inter_county, trans_county, cross_country (similar to border_type)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    origin = relationship("Location", foreign_keys=[origin_location_id], back_populates="routes_originating")
    destination = relationship("Location", foreign_keys=[destination_location_id], back_populates="routes_ending")
    shipments = relationship("Shipment", back_populates="route")
    route_group = relationship("RouteGroup", back_populates="routes")  # Each Route has one optional route_group_id. Each RouteGroup has many Routes (one-to-many). 
    route_locations = relationship("RouteLocation", back_populates="route", order_by="RouteLocation.sequence") # RouteLocation - intermediate points (bridge table)

    shipping_cost = relationship("ShippingCost", uselist=False, back_populates="route") # one-to-one
    tags = relationship('RouteTag', back_populates='route')

    @classmethod
    def create(cls, session, **kwargs):
        route = cls(**kwargs) # no need for custom __init__
        session.add(route) # no session.commit(), context manager in lib will do that for us
        return route
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, keyword):
        return session.query(cls).filter(
            cls.id == keyword
        ).first()

    def __repr__(self):
        return (f"Route: id={self.id}"
            f"origin_location_id={self.origin_location_id}"
            f"destination_location_id={self.destination_location_id}"
            f"shipping_cost={self.shipping_cost}"
            f"route_group_id={self.route_group_id}"
            f"scope={self.scope}"
            f"created_at={self.created_at}"
            f"updated_at={self.updated_at}")

```

### Other Model Files  

All other models in the project follow the same conventions as those demonstrated above. 
This includes class structure, relationships, and use of SQLAlchemy's ORM patterns.

### CLI (Comand Line Interface)  

- This is the interactive feature of the application, allowing users to navigate and perform operations via the terminal.  

- The main menu is defined in `cli.py`, located in the `app` folder.  

- `helpers.py` contains reusable functions that support CLI operations.  

- Additional menu modules are found in the `menus` folder. These provide step-by-step, procedural interaction for each domain (e.g., users, shipments, routes).  

- For reference, a sample menu implementation (`user_menu.p`y) is included below.  

```


Because our models are interconnected, and declares foreign key among themselves, we'll import all of them
in `env.py` sp that we don't run into issues. If we were to run `alembic revision --autogenerate -m "commit message"`
we will get `NoReferencedTableError` error.  

The rule is:  
> If Model A references Model B via a foreign key, then Model B must be imported in env.py

We'll therefore migrate all our models just to be on the safe side in `env.py` as so:

``` bash
from app.models.base import Base # Fortunately for us

target_metadata = Base.metadata # Metadata registration
```

Now we run `alembic revision --autogenerate -m "create users, shipments, locations, routes, route_locations, services, shipping_costs, route_groups, shipment_items, route_tags, item_categories, drop_logs, border"` from the `app`
directory to make our migration.  

After succesfull migration, yo will see something like this:
```console
$ alembic revision --autogenerate -m "create users, shipments, locations, routes, route_locations, services, shipping_costs, route_groups, shipment_items, route_tags, item_categories, drop_logs, border"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'item_categories'
INFO  [alembic.autogenerate.compare] Detected added table 'locations'
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'borders'
INFO  [alembic.autogenerate.compare] Detected added table 'route_groups'
INFO  [alembic.autogenerate.compare] Detected added table 'services'
INFO  [alembic.autogenerate.compare] Detected added table 'routes'
INFO  [alembic.autogenerate.compare] Detected added table 'route_locations'
INFO  [alembic.autogenerate.compare] Detected added table 'route_tags'
INFO  [alembic.autogenerate.compare] Detected added table 'shipments'
INFO  [alembic.autogenerate.compare] Detected added table 'shipping_costs'
INFO  [alembic.autogenerate.compare] Detected added table 'drop_logs'
INFO  [alembic.autogenerate.compare] Detected added table 'shipment_items'
  Generating /home/limassol/phase-3/dropmate_app_backend_improvement/app/migrations/versions/e912d204cd80_create_users_shipments_locations_routes_.py ...  done
```

Now do `alembic upgrade head` if all goes well to push the migrations to the database. Make sure you're in the `app` directory, the same directory we initialized alembic.   
You should see:   
```console
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 5ab19e55ccca -> e912d204cd80, create users, shipments, locations, routes, route_locations, services, shipping_costs, route_groups, shipment_items, route_tags, item_categories, drop_logs, border
```

## Relationship Definitions
We've defined our relationships **within each model class**, using the first parameter of SQLAlchemy’s `relationship()` function. 
All models are then **imported and relationships centralized** in `model.py`.  
This approach ensures that:

- Models are **fully defined before SQLAlchemy processes relationships**, allowing model strings (used as the first argument in `relationship()`) to resolve correctly.

- Circular import issues and **class registry resolution errors** are avoided.

### Recarp on Relationships:

Beyond self-referencing challenges (discussed earlier), one common issue arises when **multiple foreign keys exist between two models**. 
Let's consider an example using `Route` and `ShippingCost`.  

Suppose the `Route` model includes:
```py
shipping_cost_id = Column(Integer, ForeignKey('shipping_costs.id'), nullable=True)

and relationship definition:  
shipping_cost = relationship("ShippingCost", uselist=False, back_populates="route")
``` 

And the `ShippingCost` model also references `Route`:
```py
route_id = Column(Integer, ForeignKey('routes.id'), unique=True) 
  
and a receprocal relationship:   
route = relationship("Route", back_populates="shipping_cost")
``` 

The setup shall have introduced ambiguity. 
SQLAlchemy would raise an `AmbiguousForeignKeysError` because it wouldn't be able to determine which foreign key to use.

To fix our issue as always we would disambiguate the the foreign keys explicitly (on both sides):

```py
# in Route
shipping_cost = relationship("ShippingCost", uselist=False, back_populates="route", foreign_keys=[shipping_cost_id])

# in ShippingCost
route = relationship("Route", back_populates="shipping_cost", foreign_keys=[route_id])
```

However, a better solution might be **to consider the logical dependency between the models**.
In this case, a `ShippingCost` clearly depends on a `Route`. It makes more sense for the `Route` to "own" the relationship. So, we can simplify and clarify our design:


```py
# In Route
shipping_cost = relationship("ShippingCost", uselist=False, back_populates="route")

# In ShippingCost
route_id = Column(Integer, ForeignKey('routes.id'), unique=True)
route = relationship("Route", back_populates="shipping_cost")

```

This models the relationship cleanly:
`"A ShippingCost belongs to exactly one Route, and a Route has one optional ShippingCost."`  


## Seeding the Database

Run the seed file to populate the all the tables tables:

```console
$ python -m app.seed
```

---

## Conclusion

The power of SQLAlchemy all boils down to understanding database relationships
and making use of the correct classes and methods. By leveraging "convention
over configuration", we're able to quickly set up complex associations between
multiple models with just a few lines of code.

The **one-to-many** and **many-to-many** relationships are the most common when
working with relational databases. You can apply the same concepts and code we
used in this project to any number of different domains.

The code required to set up these relationships would look very similar to the
code we wrote in this project.

By understanding the conventions SQLAlchemy expects you to follow, and how the
underlying database relationships work, you have the ability to model all kinds
of complex, real-world concepts in your code!

---

## Menu example

```py
# app/menus/user_menu.py
from app.db import get_session
from app.modelValidation.validateUser import ValidateUser
from app.models.user import User

def user_menu():
    while True:
        print("\n-- USER MANAGEMENT --")
        print("1. Register new user")
        print("2. List all users")
        print("3. Find user by username/email")
        print("4. Delete user")
        print("   # Go Back   ")
        print("5. Back to Main Menu")
        print("   # Relationships   ")
        print("6. View user's shipments")
        print("7. View user's services")

        choice = input("Enter your choice: ")
        if choice == "5":
            break
        elif choice == "1":
            print("Registering user...")
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            find_user_by_username_or_email()
        elif choice == "4":
            delete_user_by_username()
        # (relationships)
        elif choice == "6":
            view_user_shipments()
        elif choice == "7":
            view_user_services()
        else:
            print("Invalid choice.")


def create_user():
    real_name = input("Enter your real name(first and last e.g. Jurgen Bosko): ")
    username = input("Enter your username(e.g jurgen2b): ")
    email = input("Enter your email(e.g jurgen@example.com): ")
    phone_number = input("Enter your phone number(e.g 0734567890): ")
    password = input("Enter your password(e.g secure123!A): ")
    profile_type = input("Enter your profile type(e.g customer, company, admin): ")
    
    try:
        validated_user  = ValidateUser(
            real_name=real_name, 
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            role="user",
            profile_type=profile_type # "
            )
        print(f'validated_user: {validated_user.__dict__}')

        with get_session() as session:
            user = User.create(
                session=session, # including session
                real_name=validated_user.real_name,
                username=validated_user.username,
                email=validated_user.email,
                phone_number=validated_user.phone_number,
                password=validated_user.password,
                role=validated_user.role,
                profile_type=validated_user.profile_type
            )
            print(f'User created successfully: {user}')
            print(f'New User ID: {user.id}')
            return user.id
    except Exception as exc:
        print("Error")
        print("Error creating user: ", exc)


def list_users():
    with get_session() as session: # Within the with block(just as with writting appending/to files), call get_session. Through yield session(in get_session), controle is 'passed' to with
        users = User.get_all(session) # pass session to the method
        if not users:
            print("No users found.")
        else:
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}") # with block is complete, if there are errors, they will be 'reported' back to the context manager

def find_user_by_username_or_email():
    keyword = input("Enter username or email: ")
    with get_session() as session:
        user = User.find_by_username_or_email(session, keyword)
        if user:
            print(f"User found: {user.username} | {user.email}")
            return user.id
        else:
            print("User not found.")

def delete_user_by_username():
    username = input("Enter username to delete: ")
    with get_session() as session:
        success = User.delete_by_username(session, username)
        if success:
            print("User deleted successfully.")
        else:
            print("User not found.")

# Relationships
def view_user_shipments():
    username = input("Enter username: ")
    with get_session() as session:
        user = User.find_by_username_or_email(session, username) # we have also used this in find_user_by_username_or_email func
        if not user:
            print("User not found.")
            return
        for shipment in user.shipments:
            print(f"Shipment ID: {shipment.id}, Status: {shipment.status}, Destination: {shipment.destination.name}")

def view_user_services():
    username = input("Enter username: ")
    with get_session() as session:
        user = User.find_by_username_or_email(session, username) # first find the user
        if not user:
            print("User not found.")
            return
        for service in user.services:
            print(f"Service ID: {service.id}, Company_name: {service.company_name}, Service_name: {service.service_name}, License: {service.license}")

```

---

## Resources

- [Python 3.8.13 Documentation](https://docs.python.org/3/)
- [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/en/14/orm/)
- [Alembic 1.8.1 Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [Basic Relationship Patterns - SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)
- [Running “Batch” Migrations for SQLite and Other Databases](https://alembic.sqlalchemy.org/en/latest/batch.html)