from app.models import Shipment # , ShippingCost, RouteTag, ShipmentItem, ItemCategory
from app.db import get_session
from sqlalchemy.orm import joinedload
import math

def estimate_shipping_cost_menu():
    while True:
        print("\n-- ESTIMATE SHIPPING COST FOR A SHIPMENT --")
        print("1. Seed database with mock data")
        print("2. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            estimate_shipping_cost()
        elif choice == "2":
            break
        else:
            print("Invalid choice.")

def estimate_shipping_cost():
    shipment_id = input("Enter shipment ID to estimate cost: ")

    with get_session() as session:
        shipment = session.query(Shipment).options( # .options() pre-load relationships so we don't have to query everytime
            joinedload(Shipment.route).joinedload("shipping_cost"), # shipment - route relationship
            joinedload(Shipment.route).joinedload("tags"), # route - tags relationship
            joinedload(Shipment.shipment_items).joinedload("category") # shipment - shipment items relationship. Shipment item - category relationship
        ).filter_by(id=shipment_id).first()

        if not shipment:
            print("Shipment not found.")
            return

        if not shipment.route or not shipment.route.shipping_cost: # a route has exactly 1 shipping cost
            print("Shipping cost data missing for this shipment's route.")
            return

        # 1. Base cost from route
        base_cost = shipment.route.shipping_cost.cost_value # (relationship chaining, courtesy of .options())
        print(f"\nInitial base cost for route: {base_cost}")

        # 2. Route tags (if any)
        price_factor_total = 1.0
        if shipment.route.tags:
            for tag in shipment.route.tags:
                print(f"Applying tag: {tag.tag} (factor: {tag.price_factor})")
                price_factor_total *= tag.price_factor
        else:
            print("No route tags found — using base cost as-is.")

        adjusted_base_cost = base_cost * price_factor_total
        print(f"Adjusted base cost after route tags: {adjusted_base_cost:.2f}")

        # 3. Process shipment items
        total_cost = 0
        for item in shipment.shipment_items:
            rate = item.category.base_rate if item.category else 1.0
            weight = item.weight or 1.0
            quantity = item.quantity or 1

            # Surcharge calculation (weight above 100kg)
            total_weight = weight * quantity
            surcharge = 0

            if total_weight > 100: # for weight above 100kg
                extra_kg = total_weight - 100
                extra_chunks = math.ceil(extra_kg / 100)
                surcharge = extra_chunks * 50  # fixed surcharge rate per 100kg

                # Optional: cap the surcharge
                if total_weight > 500:
                    surcharge = 2000  # cap at max 200 for weights beyond 500kg

                print(f"Weight surcharge for '{item.item_name}': {surcharge:.2f} (Extra {extra_chunks * 100}kg)")

            item_cost = (adjusted_base_cost * rate * quantity * weight) + surcharge
            print(f"Item: {item.item_name}, Qty: {quantity}, Weight: {weight}, Rate: {rate} -> Cost: {item_cost:.2f}")
            total_cost += item_cost

        print(f"\n Estimated Total Shipping Cost: {total_cost:.2f}")