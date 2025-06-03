from app.modelValidation.validateRoute import ValidateRoute
from app.models import Route 
from app.db import get_session
# from .route_location import add_location_stops # FIX IMPORT

def route_menu():
    while True:
        print("\n-- ROUTE MANAGEMENT --")
        print("1. List all routes")
        print("2. Add a new route")
        print("3. Update a route")
        print("4. Delete a route")
        print("5. View route details")
        print("   # Go Back   ")
        print("6. Back to Main Menu")
        print("  tags & location stops  ")
        print("7. Assign tags/groups to route")
        print("8. Add location stops")
        print("   # Relationships  ")
        print("9. View shipments on this route")
        print("10. View intermediate location stops")
        print("11. View tags for route")
        print("12. View shipping cost details")

        choice = input("Enter your choice: ")
        if choice == "1":
            list_routes()
        elif choice == "2":
            create_route()
        elif choice == "3":
            update_route()
        elif choice == "4":
            delete_route()
        elif choice == "5":
            find_route_by_id()
        elif choice == "6":
            break
        elif choice == "7":
            assign_tags_to_route()
        elif choice == "8":
            add_location_stops()
        elif choice == "9":
            view_shipments_for_route()
        elif choice == "10":
            view_route_stops()
        elif choice == "11":
            view_tags_for_route()
        elif choice == "12":
            view_shipping_cost_for_route()
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

def create_route():
    origin_location_id = input("Enter origin location ID (e.g. 1): ")
    destination_location_id = input("Enter destination location ID (e.g. 2): ")
    scope = input("Enter route scope (intra_city, inter_city, inter_county, trans_county, cross_country): ")
    route_group_id = input("Enter route group ID (optional): ")

    # Normalize empty string input for optional route_group_id
    route_group_id = route_group_id if route_group_id.strip() else None

    try:
        validated_route = ValidateRoute(
            origin_location_id=origin_location_id,
            destination_location_id=destination_location_id,
            scope=scope,
            route_group_id=route_group_id
        )

        print(f'validated_route: {validated_route.__dict__}')

        with get_session() as session:
            route = Route.create(
                session=session,
                origin_location_id=validated_route.origin_location_id,
                destination_location_id=validated_route.destination_location_id,
                route_group_id=validated_route.route_group_id,
                scope=validated_route.scope
            )
            print(f"Route created successfully: {route}")
            return route.id
    except Exception as e:
        print("Error creating route:", e)

def update_route():
    route_id = input("Enter route ID to update: ")
    
    with get_session() as session:
        route = Route.find_by_id(session, route_id)
        if not route:
            print("Route not found.")
            return

        print(f"Current Origin ID: {route.origin_location_id}, Destination ID: {route.destination_location_id}, Scope: {route.scope.value}, Group ID: {route.route_group_id}")
        
        origin_location_id = input("New origin location ID (Leave blank to keep current): ") or route.origin_location_id
        destination_location_id = input("New destination location ID (Leave blank to keep current): ") or route.destination_location_id
        scope = input("New scope (Leave blank to keep current): ") or route.scope.value
        route_group_id = input("New route group ID (optional): ") or route.route_group_id

        try:
            validated_route = ValidateRoute(
                origin_location_id=origin_location_id,
                destination_location_id=destination_location_id,
                scope=scope,
                route_group_id=route_group_id
            )

            route.origin_location_id = validated_route.origin_location_id
            route.destination_location_id = validated_route.destination_location_id
            route.scope = validated_route.scope
            route.route_group_id = validated_route.route_group_id

            print("Route updated successfully.")
        except Exception as e:
            print("Error updating route:", e)

def delete_route():
    route_id = input("Enter route ID to delete: ")
    with get_session() as session:
        route = Route.find_by_id(session, route_id)
        if not route:
            print("Route not found.")
            return

        session.delete(route)
        print(f"Route ID {route_id} deleted successfully.")



def list_routes():
    with get_session() as session: 
        routes = Route.get_all(session)
        if not routes:
            print("No routes found.")
        else:
            for route in routes:
                print(f"ID: {route.id}, Route_origin_location_id: {route.origin_location_id}, Route_destination_location_id: {route.destination_location_id}") # route_group_id?


def find_route_by_id():
    keyword = input("Enter route id: ")
    with get_session() as session:
        route = Route.find_by_id(session, keyword)
        if route.shipping_cost:
            print(f"Route found:")
            print(f"Origin: {route.origin.name if route.origin else route.origin_location_id}")
            print(f"Destination: {route.destination.name if route.destination else route.destination_location_id}")
            print(f"Scope: {route.scope.value}")
            print(f"Shipping Cost: {route.shipping_cost if route.shipping_cost else 'N/A'}")
            print(f"Route Group ID: {route.route_group_id}")
            print(f"Created At: {route.created_at}, Updated At: {route.updated_at}")
            return route.shipping_cost # relationship
        else:
            print("Route not found.")

# 7 Assigning Route Tag # debug
from app.models import RouteTag

def assign_tags_to_route():
    route_id = input("Enter route ID: ")
    tag = input("Enter tag (e.g., 'priority', 'fragile'): ").strip()
    price_factor_input = input("Enter price factor (default is 1.0): ").strip()

    try:
        price_factor = float(price_factor_input) if price_factor_input else 1.0
    except ValueError:
        print("Invalid price factor.")
        return

    with get_session() as session:
        route = Route.find_by_id(session, route_id)
        if not route:
            print("Route not found.")
            return

        tag_entry = RouteTag(route_id=route.id, tag=tag, price_factor=price_factor)
        session.add(tag_entry)
        print(f"Tag '{tag}' assigned to route ID {route.id} with price factor {price_factor}.")


# 8 # 8. add_location_stops() # Relyes on 
# imported from route_location.py (menu)
from app.models.route_location import RouteLocation
from app.models.location import Location

def add_location_stops():
    route_id = input("Enter route ID to add stops to: ")

    with get_session() as session:
        route = Route.find_by_id(session, route_id)
        if not route:
            print("Route not found.")
            return

        while True:
            location_id = input("Enter location ID to add as stop (or press Enter to finish): ").strip()
            if not location_id:
                break

            sequence = input("Enter sequence number for this stop: ").strip()
            try:
                sequence = int(sequence)
            except ValueError:
                print("Invalid sequence number.")
                continue

            location = Location.find_by_id(session, location_id)
            if not location:
                print("Location not found.")
                continue

            stop = RouteLocation(route_id=route.id, location_id=location.id, sequence=sequence)
            session.add(stop)
            print(f"Added stop: Location ID {location.id}, Sequence {sequence}")


# Relationships
# 9
def view_shipments_for_route():
    route_id = input("Enter route ID: ")
    with get_session() as session:
        route = Route.find_by_id(session, route_id)
        if not route:
            print("Route not found.")
            return

        if not route.shipments:
            print("No shipments found on this route.")
        else:
            for shipment in route.shipments:
                print(f"Shipment ID: {shipment.id}, Origin: {shipment.origin_location_id}, "
                      f"Destination: {shipment.destination_location_id}, Status: {shipment.status.value}")

# 10          
def view_route_stops():
    route_id = input("Enter route ID: ")
    with get_session() as session:
        route = Route.find_by_id(session, route_id)
        if not route:
            print("Route not found.")
            return

        if not route.route_locations:
            print("No intermediate stops on this route.")
            return

        print("Stops on route (in order):")
        for stop in sorted(route.route_locations, key=lambda x: x.sequence):
            print(f"Sequence {stop.sequence}: Location ID {stop.location_id} - "
                  f"{stop.location.name if stop.location else 'Unknown'}")

# 11
def view_tags_for_route():
    route_id = input("Enter route ID: ")
    with get_session() as session:
        route = Route.find_by_id(session, route_id)
        if not route:
            print("Route not found.")
            return

        if not route.tags:
            print("No tags assigned to this route.")
        else:
            print("Tags:")
            for tag in route.tags:
                print(f"Tag: {tag.tag}, Price Factor: {tag.price_factor}")

# 12
def view_shipping_cost_for_route():
    route_id = input("Enter route ID: ")
    with get_session() as session:
        route = Route.find_by_id(session, route_id)
        if not route:
            print("Route not found.")
            return

        cost = route.shipping_cost
        if not cost:
            print("No shipping cost record found for this route.")
        else:
            print(f"Shipping Cost: Base={cost.cost_value}" 
                  f"Start Date: {cost.start_date}" 
                  f"Effective Date: {cost.end_date}" 
                  f"Status: {cost.active}")
