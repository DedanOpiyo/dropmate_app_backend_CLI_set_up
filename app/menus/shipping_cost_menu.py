from app.modelValidation.validateShippingCost import ValidateShippingCost
from app.models.shippingCost import ShippingCost  
from app.db import get_session 

def create_shipping_cost():
    route_id = input("Enter route ID (e.g. 3): ")
    cost_value = input("Enter cost value (e.g. 250): ")
    start_date = input("Enter start date (YYYY-MM-DD) or leave blank: ")
    end_date = input("Enter end date (YYYY-MM-DD) or leave blank: ")
    active_input = input("Is this cost active? (yes/no): ")

    try:
        active = active_input.strip().lower() in ['yes', 'y', 'true', '1']
        validated_cost = ValidateShippingCost(
            route_id=route_id,
            cost_value=cost_value,
            start_date=start_date,
            end_date=end_date,
            active=active
        )
        print(f'validated_cost: {validated_cost.__dict__}')

        with get_session() as session:
            shipping_cost = ShippingCost.create(
                session=session,
                route_id=validated_cost.route_id,
                cost_value=validated_cost.cost_value,
                start_date=validated_cost.start_date,
                end_date=validated_cost.end_date,
                active=validated_cost.active
            )
            print(f"Shipping cost created successfully: {shipping_cost}")
            return shipping_cost.id
    except Exception as exc:
        print("Error")
        print("Error creating shipping cost:", exc)
