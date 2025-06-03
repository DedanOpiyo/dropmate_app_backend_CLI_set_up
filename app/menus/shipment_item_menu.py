from app.modelValidation.validateShipmentItem import ValidateShipmentItem
from app.models.shipmentItem import ShipmentItem
from app.db import get_session

def handle_add_shipment_items(shipment_id): # add_items_for_current_shipment
    while True:
        print("\n-- ADD SHIPMENT ITEM --")
        item_name = input("Item name (e.g. Laptop.5): ")
        quantity = input("Quantity (e.g. 2): ")
        description = input("Description (e.g. 2.15-inch MacBook Pro): ")
        weight = input("Weight (e.g. 2.5): ")
        value = input("Value (e.g. 2000): ")
        category_id = input("Category ID: ")

        try:
            validated_item = ValidateShipmentItem(
                shipment_id=shipment_id,
                item_name=item_name,
                description=description,
                weight=weight,
                quantity=quantity,
                value=value,
                category_id=category_id
            )

            with get_session() as session:
                item = ShipmentItem.create(
                    session=session,
                    shipment_id=validated_item.shipment_id,
                    item_name=validated_item.item_name,
                    description=validated_item.description,
                    weight=validated_item.weight,
                    quantity=validated_item.quantity,
                    value=validated_item.value,
                    category_id=validated_item.category_id
                )
            print(f"Shipment item saved: {item}")
        except Exception as e:
            print("Error adding item:", e)

        more = input("Add another item? (y/n): ")
        if more.lower() != 'y':
            break
