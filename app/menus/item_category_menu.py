# Direct interaction using alchemy, other menus used class methods such as create etc.
from app.modelValidation.validateItemCategory import ValidateItemCategory
from app.models import ItemCategory
from app.db import get_session
import logging

def item_category_menu():
    while True:
        print("\n-- ITEM CATEGORY MANAGEMENT --")
        print("1. List all item categories")
        print("2. Add a new item category")
        print("3. Update an item category")
        print("4. Delete an item category")
        print("   # Go Back   ")
        print("5. Back to Main Menu")
        print("   # Relationships   ")
        print("6. View shipment items by/for a category")

        choice = input("Enter your choice: ")
        if choice == "1":
            logging.info("Option 1 selected")
            list_item_categories()
        elif choice == "2":
            create_item_category()
        elif choice == "3":
            update_item_category()
        elif choice == "4":
            delete_item_category()
        elif choice == "6":
            view_items_by_category()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# logging.info("Logging something...") 
def list_item_categories():
    with get_session() as session:
        categories = session.query(ItemCategory).all()
        if not categories:
            print("No item categories found.")
        else:
            for cat in categories:
                print(f"ID: {cat.id}, Name: {cat.name}, Base Rate: {cat.base_rate}, Description: {cat.description}")

def create_item_category():
    name = input("Enter category name: ")
    base_rate = input("Enter base rate (default 1.0): ")
    description = input("Enter description (optional): ")

    try:
        validated = ValidateItemCategory(name, base_rate, description)
        with get_session() as session:
            category = ItemCategory( # For the ItemCategory we can use the class directly other than create(class method) we've been using. No ned to pass session param
                name=validated.name,
                base_rate=validated.base_rate,
                description=validated.description
            )
            session.add(category)
            session.push()
            print(f"Item category '{category.name}' added with ID {category.id}.")
    except Exception as e:
        print("Error:", e)

def update_item_category():
    cat_id = input("Enter category ID to update: ")
    with get_session() as session:
        category = session.query(ItemCategory).filter_by(id=cat_id).first()
        if not category:
            print("Category not found.")
            return

        print(f"Current Name: {category.name}, Base Rate: {category.base_rate}, Description: {category.description}")

        new_name = input("New name (leave blank to keep current): ") or category.name
        new_base_rate = input("New base rate (leave blank to keep current): ") or category.base_rate
        new_desc = input("New description (leave blank to keep current): ") or category.description

        try:
            validated = ValidateItemCategory(new_name, new_base_rate, new_desc)
            category.name = validated.name
            category.base_rate = validated.base_rate
            category.description = validated.description
            print("Category updated.")
        except Exception as e:
            print("Error:", e)

def delete_item_category():
    cat_id = input("Enter category ID to delete: ")
    with get_session() as session:
        category = session.query(ItemCategory).filter_by(id=cat_id).first()
        if not category:
            print("Category not found.")
            return
        session.delete(category)
        print(f"Item category ID {cat_id} deleted.")

# Relationship
def view_items_by_category():
    cat_id = input("Enter category ID: ")
    with get_session() as session:
        category = session.query(ItemCategory).filter_by(id=cat_id).first()
        if not category:
            print("Category not found.")
            return
        if not category.shipment_items:
            print("No shipment items in this category.")
            return
        for item in category.shipment_items:
            print(f"ShipmentItem ID: {item.id}, Shipment ID: {item.shipment_id}, Quantity: {item.quantity}")


