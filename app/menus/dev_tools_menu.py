import subprocess  # Importing subprocess to call seed.py

def dev_tools_menu():
    while True:
        print("\n-- DEVELOPER TOOLS --")
        print("1. Seed database with mock data")
        print("2. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            run_seeder()
        elif choice == "2":
            break
        else:
            print("Invalid choice.")

def run_seeder():
    print("\nSeeding database with mock data...\n")
    try:
        # Running your seed.py script via the module # subprocess.run([rte"], check=True)
        result = subprocess.run(
            ["python", "-m", "app.seed"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(result.stdout)
        print("DB Seeding completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error occurred while seeding the database:", e)
