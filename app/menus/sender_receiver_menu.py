from app.modelValidation.validateShipmentContactInfo import ValidateShipmentContactInfo
from app.models.shipmentContactInfo import ShipmentContactInfo
from app.db import get_session

def handle_sender_receiver_input(shipment_data):
    print("\n-- SENDERT & REVEIVER INFO --")
    shipment_id = shipment_data.get("shipment_id", "0")
    info_provider_id = shipment_data.get("user_id", "0")
    print(f"handle_sender_receiver_input called: {shipment_id}")

    sender_name = input("Sender Name: ")
    sender_phone = input("Sender Phone: ")
    sender_address = input("Sender Address: ")

    receiver_name = input("Receiver Name: ")
    receiver_phone = input("Receiver Phone: ")
    receiver_address = input("Receiver Address: ")

    try:
        validated = ValidateShipmentContactInfo(
            shipment_id=shipment_id,
            sender_name=sender_name,
            sender_phone=sender_phone,
            sender_address=sender_address,
            receiver_name=receiver_name,
            receiver_phone=receiver_phone,
            receiver_address=receiver_address,
            info_provider_id=info_provider_id
        )
        with get_session() as session:
            shipment_contact_info = ShipmentContactInfo.create(
                shipment_id=validated.shipment_id,
                sender_name=validated.sender_name,
                sender_phone=validated.sender_phone,
                sender_address=validated.sender_address,
                receiver_name=validated.receiver_name,
                receiver_phone=validated.receiver_phone,
                receiver_address=validated.receiver_address,
                nfo_provider_id=validated.info_provider_id
            )
            print(f"Sender and receiver info - (Shipment_contact_info) created successfully: {shipment_contact_info}")
            return shipment_contact_info.id
    except Exception as e:
        print("Validation failed:", e)
