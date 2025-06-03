# app/menus/manage_shipments.py
from app.db import get_session
# from app.modelValidation.validateUser import ValidateUser
from app.models.shipment import Shipment, ShipmentStatus
from app.models.drop_log import DropLog

def shipment_management_menu():
    while True:
        print("\n-- SHIPMENT MANAGEMENT --")
        print("1. List all shipments")
        print("2. Track shipment by ID")
        print("3. Update shipment status")
        print("4. Delete shipment")
        print("   # Go Back   ")
        print("5. Back to Main Menu")
        print("   # Relationships  ")
        print("6. Check if shipment has crossed border")
        print("7. Check delivery status via DropLog")

        choice = input("Enter your choice: ")
        if choice == "5":
            break
        elif choice == "1":
            print("List all shipments...")
            list_shipments()
        elif choice == "2":
            track_shipment_by_id()
        elif choice == "3":
            update_shipment_status()
        elif choice == "4":
            delete_shipment()
        # Other cases to follow (relationships)
        elif choice == "6":
            check_shipment_border_crossing()
        elif choice == "7":
            check_drop_log_status()
        else:
            print("Invalid choice.")


def list_shipments():
    with get_session() as session:
        shipments = Shipment.get_all(session)
        if not shipments:
            print("No shipments found.")
        else:
            for shipment in shipments:
                print(f"ID: {shipment.id}"  
                      f"User_id: {shipment.user_id}"  
                      f"Origin_location_id: {shipment.origin_location_id}"  
                      f"destination_location_id: {shipment.destination_location_id}"
                      f"Route_id: {shipment.route_id}"
                      f"Service_id: {shipment.service_id}"
                      f"Status: {shipment.status}"
                      f"Shipment_type: {shipment.shipment_type}"
                      f"Shipping_cost: {shipment.shipping_cost}") 

def track_shipment_by_id():
    id = input("Enter shipment id: ")
    with get_session() as session:
        shipment = Shipment.find_by_id(session, id)
        if shipment:
            print(f"Shipment found: ID: {shipment.id}" 
                f"Origin_location_id: {shipment.origin_location_id}"   
                f"destination_location_id: {shipment.destination_location_id}" 
                f"Route_id: {shipment.route_id}" 
                f"Service_id: {shipment.service_id}" 
                f"Status: {shipment.status}" 
                f"Shipment_type: {shipment.shipment_type}")
            return shipment
        else:
            print("Shipment not found.")

def update_shipment_status():
    shipment_id = input("Enter the ID of the shipment to update: ").strip()
    new_status = input("Enter the new status (pending, in transit, delivered): ").strip().lower()
    
    if new_status not in {status.value for status in ShipmentStatus}: # chaining ._value2member_map_
        print(f"Invalid status '{new_status}'. Allowed: {', '.join(s.value for s in ShipmentStatus)}")
        return

    with get_session() as session:
        shipment = Shipment.find_by_id(session, shipment_id)
        if not shipment:
            print("Shipment not found.")
            return

        shipment.status = ShipmentStatus(new_status)
        session.add(shipment)
        print(f"Shipment ID {shipment_id} status updated to '{new_status}'.")

# contact info table needed for this
def delete_shipment():
    shipment_id = input("Enter the ID of the shipment to delete: ").strip()

    with get_session() as session:
        success = Shipment.delete_by_id(session, shipment_id)
        if success:
            print(f"Shipment ID {shipment_id} and related data deleted successfully.")
        else:
            print("Shipment not found or could not be deleted.")

def check_shipment_border_crossing():
    shipment_id = input("Enter shipment ID: ")
    with get_session() as session:
        shipment = session.get(Shipment, int(shipment_id))
        if not shipment:
            print("Shipment not found.")
            return

        # Check route locations for any with is_border=True
        locations = shipment.route.route_locations
        border_locs = [rl.location.name for rl in locations if rl.location.is_border]
        if border_locs:
            print("This shipment crosses borders at:", ", ".join(border_locs))
        else:
            print("No border crossings on this route.")

def check_drop_log_status():
    shipment_id = input("Enter shipment ID: ")
    with get_session() as session:
        logs = session.query(DropLog).filter(DropLog.shipment_id == int(shipment_id)).order_by(DropLog.created_at).all()
        if not logs:
            print("No logs for this shipment.")
            return
        for log in logs:
            print(f"{log.created_at} - {log.status} at {log.location}")

