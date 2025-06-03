from app.models.location import Location, LocationType
from app.db import get_session

def location_menu():
    while True:
        print("\n-- LOCATION MANAGEMENT --")
        print("1. List all locations")
        print("2. Add a new location")
        print("3. Update location")
        print("4. Delete location")
        print("5. View borders")
        print("   # Go Back   ")
        print("6. Back to Main Menu")
        print("   # Relationships  ")
        print("7. View shipments from this location")
        print("8. View shipments arriving at this location")
        print("9. View routes starting here")
        print("10. View routes ending here")
        print("11. Get full hierarchy of a location")
        print("12. View children/contained locations")
        print("13. View route groups for location")

        choice = input("Enter your choice: ")
        if choice == "1":
            list_locations()
        elif choice == "2":
            add_location()
        elif choice == "3":
            update_location()
        elif choice == "4":
            delete_location()
        elif choice == "5":
            view_borders()
        elif choice == "6":
            break
        elif choice == "7":
            view_shipments_from_location()
        elif choice == "8":
            view_shipments_arriving_at_location()
        elif choice == "9":
            view_routes_starting_here()
        elif choice == "10":
            view_routes_ending_here()
        elif choice == "11":
            location_hierarchy()
        elif choice == "12":
            view_children_locations()
        elif choice == "13":
            view_route_groups_for_location()
        else:
            print("Invalid choice.")

def list_locations():
    with get_session() as session:
        locations = Location.get_all(session)
        if not locations:
            print("No locations found.")
        else:
            for loc in locations:
                print(f"ID: {loc.id}, Name: {loc.name}, Type: {loc.type.value}, Country ID: {loc.country_id}, Is Border: {loc.is_border}")


def add_location():
    name = input("Enter location name: ")
    print("Select type: " + ", ".join(t.value for t in LocationType))
    type_input = input("Enter location type: ").strip().lower()
    type_enum = next((t for t in LocationType if t.value == type_input), None)

    if not type_enum:
        print("Invalid location type.")
        return

    constituency = input("Enter constituency: ")
    is_border = input("Is this a border location? (y/n): ").strip().lower() == 'y'

    with get_session() as session:
        location = Location.create(
            session,
            name=name,
            type=type_enum,
            constituency=constituency,
            is_border=is_border
        )
        print(f"Location '{location.name}' added with ID {location.id}.")


def update_location():
    location_id = input("Enter location ID to update: ").strip()
    with get_session() as session:
        location = Location.find_by_id(session, location_id)
        if not location:
            print("Location not found.")
            return

        new_name = input(f"New name (Leave blank to keep '{location.name}'): ")
        if new_name:
            location.name = new_name

        print("Select new type or press Enter to keep current: " + ", ".join(t.value for t in LocationType))
        new_type_input = input(f"Current type is '{location.type.value}': ").strip().lower()
        if new_type_input:
            new_type = next((t for t in LocationType if t.value == new_type_input), None)
            if new_type:
                location.type = new_type
            else:
                print("Invalid type. Skipping type update.")

        print("Location updated.")


def delete_location():
    location_id = input("Enter location ID to delete: ").strip()
    with get_session() as session:
        success = Location.delete_by_id(session, location_id)
        if success:
            print(f"Location ID {location_id} deleted successfully.")
        else:
            print("Location not found or could not be deleted.")


def view_borders():
    with get_session() as session:
        borders = session.query(Location).filter_by(is_border=True).all()
        if not borders:
            print("No border locations found.")
        else:
            for loc in borders:
                print(f"ID: {loc.id}, Name: {loc.name}, Type: {loc.type.value}")

# Relationships

# utility func
def get_location_by_name(session, name):
    return session.query(Location).filter(Location.name.ilike(name)).first()

# 7. View shipments from this location
def view_shipments_from_location():
    name = input("Enter origin location name: ")
    with get_session() as session:
        loc = get_location_by_name(session, name)
        if not loc:
            print("Location not found.")
            return

        if not loc.shipments_originating:
            print("No shipments found from this location.")
        else:
            for shipment in loc.shipments_originating:
                print(f"Shipment ID: {shipment.id}, Destination: {shipment.destination_location_id}, Status: {shipment.status.value}")

# 8. View shipments arriving at this location
def view_shipments_arriving_at_location():
    name = input("Enter destination location name: ")
    with get_session() as session:
        loc = get_location_by_name(session, name)
        if not loc:
            print("Location not found.")
            return

        if not loc.shipments_arriving:
            print("No shipments arriving at this location.")
        else:
            for shipment in loc.shipments_arriving:
                print(f"Shipment ID: {shipment.id}, Origin: {shipment.origin_location_id}, Status: {shipment.status.value}")

# 9. View routes starting here
def view_routes_starting_here():
    name = input("Enter origin location name: ")
    with get_session() as session:
        loc = get_location_by_name(session, name)
        if not loc:
            print("Location not found.")
            return

        if not loc.routes_originating:
            print("No routes originate from this location.")
        else:
            for route in loc.routes_originating:
                print(f"Route ID: {route.id}, Destination: {route.destination_location_id}")

# 10. View routes ending here
def view_routes_ending_here():
    name = input("Enter destination location name: ")
    with get_session() as session:
        loc = get_location_by_name(session, name)
        if not loc:
            print("Location not found.")
            return

        if not loc.routes_ending:
            print("No routes end at this location.")
        else:
            for route in loc.routes_ending:
                print(f"Route ID: {route.id}, Origin: {route.origin_location_id}")

# 11. Get full hierarchy of a location
def location_hierarchy():
    name = input("Enter location name: ")
    with get_session() as session:
        loc = get_location_by_name(session, name)
        if not loc:
            print("Location not found.")
            return
        chain = []
        while loc:
            chain.append(loc.name)
            loc = loc.parent
        print(" > ".join(reversed(chain)))

# 12. View children/contained locations
def view_children_locations():
    name = input("Enter location name: ")
    with get_session() as session:
        loc = get_location_by_name(session, name)
        if not loc:
            print("Location not found.")
            return
        if not loc.children and not loc.contained_locations:
            print("No children or contained locations.")
            return

        print(f"Direct children (hierarchical): {[child.name for child in loc.children]}")
        print(f"Contained by country relationship: {[child.name for child in loc.contained_locations]}")

# 13. View route groups for location
def view_route_groups_for_location():
    name = input("Enter location name: ")
    with get_session() as session:
        loc = get_location_by_name(session, name)
        if not loc:
            print("Location not found.")
            return
        if not loc.route_groups:
            print("No route groups for this location.")
            return

        for rg in loc.route_groups:
            print(f"Route Group ID: {rg.id}, Name: {rg.name}")




