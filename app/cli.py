# app/cli.py

from app.menus.user_menu import user_menu
from app.menus.shipment_menu import new_shipment_menu
from app.menus.manage_shipments import shipment_management_menu
from app.menus.location_menu import location_menu
from app.menus.route_menu import route_menu
from app.menus.item_category_menu import item_category_menu
from app.menus.estimate_shipping_cost_menu import estimate_shipping_cost_menu

from app.menus.dev_tools_menu import dev_tools_menu


from app.helpers import (
    exit_program, helper_1
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            user_menu()
        elif choice == "2":
            new_shipment_menu()
        elif choice == "3":
            shipment_management_menu()
        elif choice == "4":
            route_menu()
        elif choice == "5":
            item_category_menu()
        elif choice == "6":
            location_menu()
        elif choice == "7":
            estimate_shipping_cost_menu()
        elif choice == "8":
            dev_tools_menu()
        elif choice == "98":
            helper_1()
        else:
            print("Invalid choice")


# Main Menu (Top-Level)
def menu():
    print("\n=== DropMate CLI ===")
    print("Please select an option:")
    print("0. Exit the program")
    print("1. User Account Management (Login/create account)")
    print("2. Create New Shipment")
    print("3. Manage Shipments")
    print("4. View/Manage Routes")
    print("5. Categories & Items")
    print("6. Locations")
    print("7. Shipping Cost Estimation")
    print("8. Developer Tools / Debug")
    print("98. Help")


if __name__ == "__main__":
    main()
