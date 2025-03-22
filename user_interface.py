from Truck import Truck
import time
from Package import Package


# User Interface
def display(truck1, truck2, truck3, trucks, truck_table, incorrect_addresses, delayed_packages, addresses):
    while True:
        print("\n\n\033[1mWGUPS Package Tracker Software\033[0m")
        print("*" * 50)
        print("1. Get Truck Total Mileage")
        print("2. Get a Single Package Status with a Time")
        print("3. Get All Package Status with a Time")
        print("4. Exit the Program")
        print("*" * 50)

        try:
            reader = input("\nEnter your selection (1-4), or 'b' for main menu: ").strip().lower()
            if reader in ['4', 'q', 'exit']:
                print("Exiting program...")
                time.sleep(2)
                exit()

            elif reader == '3':
                package_time = input("\nType a time to view all package statuses (format: 10:00 AM): ").lower()
                if package_time.lower() == 'b':
                    continue
                if "am" not in package_time.split() and "pm" not in package_time.split():
                    confirm = input("\nEnter AM or PM: ")
                    if confirm.lower() == 'b':
                        continue
                    pkg_time = package_time.split(" ")
                    pkg_time.append(confirm)
                    package_time = " ".join(pkg_time)
                try:
                    print(Package.get_all_package_status(package_time, truck1, truck2, truck3, trucks, incorrect_addresses, delayed_packages, addresses))
                except ValueError as e:
                    print("Invalid time format. (xx:xx AM/PM)")

            elif reader == '2':
                p_id = input("Enter package ID: ").strip()
                if p_id.lower() == 'b':
                    continue
                if not p_id.isdigit():
                    print("Invalid packaage ID: Please enter a package ID 1-40")
                    continue
                p_id = int(p_id)
                package_time = input("Enter a time to view package {}'s status: ".format(p_id))
                if package_time.lower() == 'b':
                    continue

                if "am" not in package_time.split(" ") and "pm" not in package_time.split():
                    confirm = input("\nEnter AM or PM: ")
                    if confirm.lower() == 'b':
                        continue
                    pkg_time = package_time.split()
                    pkg_time.append(confirm)
                    package_time = " ".join(pkg_time)
                try:
                    print("\n\033[1mSingle Package Report With a Time:\033[0m")
                    print("=" * 170)
                    print(Package.get_package_status(p_id, package_time, truck1, truck2, truck3, trucks, incorrect_addresses, delayed_packages, addresses))
                except ValueError as e:
                    print("Invalid time format. (xx:xx AM/PM)")
            elif reader == '1':
                print(Truck.get_mileage(truck_table))
                
            if reader not in ['1','2','3','4','exit','q']:
                print("Enter a valid option.")
            if reader == 'b':
                try:
                    continue
                except ValueError as e:
                    pass
        except Exception as e:
            print("An error occurred: {}".format(e))