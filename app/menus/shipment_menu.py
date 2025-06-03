# app/menus/shipment_menu.py
from app.db import get_session
from app.models.shipment import Shipment
from app.menus.sender_receiver_menu import handle_sender_receiver_input
from app.menus.shipment_item_menu import handle_add_shipment_items # used in step 5
from app.menus.user_menu import create_user # find_user_by_username_or_email, 
from app.menus.route_menu import create_route # used in 1
from app.menus.shipping_cost_menu import create_shipping_cost # used in 2
from app.modelValidation.validateShipment import ValidateShipment
from app.menus.route_menu import find_route_by_id # used in 2
from app.models.user import User # used in create_shipment(), step 3

shipment_data = {}  # Temporary in-memory store for shared state # Dictionary mapping other than nesting if else

# Reusable input function
def prompt_for_missing_required_id(id_type):
    print(f"To add shipment you need a valid {id_type.capitalize()} ID.")
    choice = input(f"Would you like to enter a {id_type.capitalize()} ID manually, search for it, or go back? (enter/search/back): ").strip().lower()
    if choice == "enter": # if user knows attribute/row id
        entered_id = input(f"Enter existing {id_type.capitalize()} ID: ").strip()
        if entered_id.isdigit():
            shipment_data[f"{id_type}_id"] = entered_id
            print(f"{id_type.capitalize()} ID recorded.")
            # what next ?
        else:
            print(f"Invalid {id_type}. Must be a number.")
    elif "search": # if user wants to search for attribute/row id
        if id_type == 'route':
            print("search feature coming soon.") # route_id
            return
        elif id_type == 'user':
            print("search feature coming soon.") # user_id
            return
        elif id_type == 'shipment': 
            print("search feature coming soon.") # shipment_id
            return 
        print("No search feature yet. Returning to shipment menu...")
    else:
        print("Returning to shipment menu...")

def create_shipment():
    if not shipment_data.get('route_id'):
        print('You must complete step 1 to register shipment')
        return # early returns on missing critical data (steps 2)

    if not shipment_data.get('shipping_cost'):
        print('You must complete step 2 to register shipment')
        return # early returns on missing critical data (steps 3)

    choice = input("Do you have a User ID? (y/n): ").strip().lower()
    if choice == "y":
        print("Registering shipment...")
        prompt_for_missing_required_id('user')
    elif choice == "n":
        print("Registering User to get ID...")
        user_id = create_user()
        if user_id:
            shipment_data["user_id"] = user_id
            print(f"User Id : ({shipment_data["user_id"]}) saved succesfully")
        else:
            print("Could not create user, try again")
            return

    print("Creating shipment...")
    origin_location_id = input("Enter origin_location_id: ")
    destination_location_id = input("Enter destination_location_id: ")
    service_id = input("Enter service_id: ")
    status = input("Enter status: ")
    shipment_type = input("Enter shipment_type: ")

    if shipment_type:
        print({
            "user_id": shipment_data.get("user_id"),
            "origin_location_id": origin_location_id,
            "destination_location_id": destination_location_id,
            "route_id": shipment_data.get("route_id"),
            "service_id": service_id
        })

        try:
            validated_shipment = ValidateShipment(
                user_id=shipment_data["user_id"],
                origin_location_id=origin_location_id,
                destination_location_id=destination_location_id,
                route_id=shipment_data["route_id"],
                service_id=service_id,
                status=status, # e.g. 'in transit'
                shipment_type=shipment_type, # e.g. 'goods'
                shipping_cost=shipment_data["shipping_cost"]
            )
            print("PASS: Validation with string IDs succeeded.")
            print(vars(validated_shipment))

            with get_session() as session:
                shipment = Shipment.create(
                    session=session, # include session
                    user_id=validated_shipment.user_id,
                    origin_location_id=validated_shipment.origin_location_id,
                    destination_location_id=validated_shipment.destination_location_id,
                    route_id=validated_shipment.route_id,
                    service_id=validated_shipment.service_id,
                    status=validated_shipment.status,
                    shipment_type=validated_shipment.shipment_type,
                    shipping_cost=validated_shipment.shipping_cost
                )
                print(f'Shipment created successfully: {shipment}')
                return shipment.id
        except Exception as exc:
            print("Error")
            print("Error creating shipment:", exc)

def new_shipment_menu():
    while True:
        print("\n-- NEW SHIPMENT --")
        print("1. Assign route")
        print("2. Register Base-shipping-cost")
        print("3. Register shipment") # persist shipment, then add items
        print("4. Add shipment items") # needs step 4, but there is quick manual option
        print("5. Enter sender & receiver info")
        print("6. View Reference Data")
        print("   # Go Back   ")
        print("7. Cancel & return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            choice = input("Do you have a Route ID? (yes/search/create one): ").strip().lower()
            if choice == "yes" or "search":
                prompt_for_missing_required_id('route')
            elif choice == "create one":
                route_id = create_route()
                if route_id:
                    shipment_data["route_id"] = route_id
                else:
                    print("Could not create route, try again")
                    break

        elif choice == "2":
            if not shipment_data["route_id"]:
                print("To add a shipping cost, you need to complete step 2")
                break # end early if no route id
            
            choice = input("Do you have a Base/Shipping Cost for the Route? (yes/search/add one): ").strip().lower()
            
            if choice == "yes":
                shipping_cost = input(f"Enter Shipping Cost for the route ({shipment_data["route_id"]}): ")
                if shipping_cost:
                    shipment_data["shipping_cost"] = shipping_cost
                else:
                    print("could not validate the provided shipping cost, retry.")
                    break 
            elif choice == "search":
                shipping_cost = find_route_by_id(shipment_data["route_id"])
                if shipping_cost:
                    shipment_data["shipping_cost"] = shipping_cost 
                else:
                    print("Sorry, could not find shipping cost, please retry")
                    break 
            elif choice == "add one":
                print(f"{'Create shipping cost'.capitalize()} using the Route ID: {shipment_data.get('route_id')}") # we should already have route_id from step 2
                shipping_cost_id = create_shipping_cost()
                if shipping_cost_id:
                    shipment_data["shipping_cost_id"] = shipping_cost_id
                else:
                    print("Could not create shipping cost, try again")
                    break

        elif choice == "3":
            key_value_list = [[key, value] for key, value in shipment_data.items()]
            print(f"DEBUGGING THE SHIPMENT_DATA {key_value_list}")
            
            shipment_id = create_shipment() # create/register shipment
            if shipment_id:
                shipment_data["shipment_id"] = shipment_id

        elif choice == "4":
            if "shipment_id" not in shipment_data:
                prompt_for_missing_required_id('shipment')
            if "shipment_id" in shipment_data: # good news, you can complete step 5 without having to complete step 4
                handle_add_shipment_items(shipment_data["shipment_id"])

        if choice == "5":
            if not shipment_data.get('user_id'):
                print("Please complete step 3 (Register shipment) to continue")
                break
            handle_sender_receiver_input(shipment_data) # shipment_contact_info

        elif choice == "6":
            print("Reference data viewer coming soon.")  # Placeholder

        elif choice == "7":
            print("Cancelling shipment...")
            shipment_data.clear()
            break

        else:
            print("Invalid choice.")


# # chice 3
# you need info on routes
# info on route tags
# info on item category(base cost)





# # app/models/shipment.py
# from .base import Base  # relative import
# from enum import Enum as PyEnum
# class ShipmentStatus(PyEnum):
#     pending = "pending"
#     in_transit = "in transit"
#     delivered = "delivered"

# class ShipmentType(PyEnum):
#     goods = "goods"
#     person = "person"

# class Shipment(Base):
#     __tablename__ = 'shipments'
#     id = Column(Integer(), primary_key=True)
#     user_id = Column(Integer(), ForeignKey('users.id')) # Reference users table as shipments(attribute). User can have many shipments- through multiple rows
#     origin_location_id = Column(Integer, ForeignKey('locations.id')) # many-to-one. In this column many rows may point to same origin_location_id. Many shipments can originate from one location
#     destination_location_id = Column(Integer(), ForeignKey('locations.id'))
#     route_id = Column(Integer, ForeignKey('routes.id'))
#     service_id = Column(Integer(), ForeignKey('services.id'))
#     status = Column(Enum(ShipmentStatus), nullable=False, default=ShipmentStatus.pending)  # pending, in transit, delivered
#     shipment_type = Column(Enum(ShipmentType), default=ShipmentType.goods) # goods, person
#     shipping_cost = Column(Integer())
#     created_at = Column(DateTime(), server_default=func.now())
#     updated_at = Column(DateTime(), onupdate=func.now())

#     # Relationships
#     user = relationship('User', backref='shipments')
#     service = relationship('Service', back_populates="shipments")
#     origin = relationship('Location', foreign_keys=[origin_location_id], back_populates='shipments_originating') # disambiguate the FK column in the relationship since there are multiple FKs to the same table - Location.
#     destination = relationship('Location', foreign_keys=[destination_location_id], back_populates='shipments_arriving') # simple unidirectional relationship since I don’t need a reverse relationship from target model - Locatn(back to shipment)
#     route = relationship('Route', back_populates='shipments') # Many-to-one. One Shipment uses one Route. One Route can be used by many Shipments
#     shipment_items = relationship('ShipmentItem', back_populates='shipment') #-Base rate on an item is available from its category(* no. of items)
#     drop_logs = relationship('DropLog', back_populates='shipment')