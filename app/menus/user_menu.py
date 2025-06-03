# app/menus/user_menu.py
from app.db import get_session
from app.modelValidation.validateUser import ValidateUser
from app.models.user import User

def user_menu():
    while True:
        print("\n-- USER MANAGEMENT --")
        print("1. Register new user")
        print("2. List all users")
        print("3. Find user by username/email")
        print("4. Delete user")
        print("   # Go Back   ")
        print("5. Back to Main Menu")
        print("   # Relationships   ")
        print("6. View user's shipments")
        print("7. View user's services")

        choice = input("Enter your choice: ")
        if choice == "5":
            break
        elif choice == "1":
            print("Registering user...")
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            find_user_by_username_or_email()
        elif choice == "4":
            delete_user_by_username()
        # Other cases to follow (relationships)
        elif choice == "6":
            view_user_shipments()
        elif choice == "7":
            view_user_services()
        else:
            print("Invalid choice.")


def create_user():
    real_name = input("Enter your real name(first and last e.g. Jurgen Bosko): ")
    username = input("Enter your username(e.g jurgen2b): ")
    email = input("Enter your email(e.g jurgen@example.com): ")
    phone_number = input("Enter your phone number(e.g 0734567890): ")
    password = input("Enter your password(e.g secure123!A): ")
    profile_type = input("Enter your profile type(e.g customer, company, admin): ")
    
    try:
        validated_user  = ValidateUser(
            real_name=real_name, 
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            role="user",
            profile_type=profile_type # "customer"  # Can be a string or ProfileType.customer
            )
        print(f'validated_user: {validated_user.__dict__}')

        with get_session() as session:
            user = User.create(
                session=session, # including session
                real_name=validated_user.real_name,
                username=validated_user.username,
                email=validated_user.email,
                phone_number=validated_user.phone_number,
                password=validated_user.password,
                role=validated_user.role,
                profile_type=validated_user.profile_type
            )
            print(f'User created successfully: {user}')
            print(f'New User ID: {user.id}')
            return user.id
    except Exception as exc:
        print("Error")
        print("Error creating user: ", exc)


def list_users():
    with get_session() as session: # within the with block(just as with writting appending/to files), call get_session. Through the yield session, controle is handled to with
        users = User.get_all(session) # pass session to the method
        if not users:
            print("No users found.")
        else:
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}") # with block is complete, if there are errors, they will be 'reported' back to the context manager


def find_user_by_username_or_email():
    keyword = input("Enter username or email: ")
    with get_session() as session:
        user = User.find_by_username_or_email(session, keyword)
        if user:
            print(f"User found: {user.username} | {user.email}")
            return user.id
        else:
            print("User not found.")


def delete_user_by_username():
    username = input("Enter username to delete: ")
    with get_session() as session:
        success = User.delete_by_username(session, username)
        if success:
            print("User deleted successfully.")
        else:
            print("User not found.")


# Relationships
def view_user_shipments():
    username = input("Enter username: ")
    with get_session() as session:
        user = User.find_by_username_or_email(session, username) # we have also used this in find_user_by_username_or_email func
        if not user:
            print("User not found.")
            return
        for shipment in user.shipments:
            print(f"Shipment ID: {shipment.id}, Status: {shipment.status}, Destination: {shipment.destination.name}")

def view_user_services():
    username = input("Enter username: ")
    with get_session() as session:
        user = User.find_by_username_or_email(session, username) # first find the user
        if not user:
            print("User not found.")
            return
        for service in user.services:
            print(f"Service ID: {service.id}, Company_name: {service.company_name}, Service_name: {service.service_name}, License: {service.license}")
