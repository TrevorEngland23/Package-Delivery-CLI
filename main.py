# Trevor England
# Student ID: 011979246

from HashTable import HashTable
from data_loader import load_package_data, load_distance_data, load_address_data
from Truck import Truck
import user_interface


def main():
    # Initialize the package hash table
    package_table = HashTable()

    # Initialize the truck hash table
    truck_table = HashTable(size=3)

    # Load data
    load_package_data(package_table)
    distances = load_distance_data()
    addresses = load_address_data()

    # Instantiate Trucks
    truck1 = Truck(truck_id=1, driver_id=1)
    truck2 = Truck(truck_id=2, start_time="9:15 AM",driver_id=2)
    truck3 = Truck(truck_id=3, start_time="10:30 AM", driver_id=1)

    # Insert truck data in truck hash table
    truck_table.insert(truck1.truck_id, 0.0)
    truck_table.insert(truck2.truck_id, 0.0)
    truck_table.insert(truck3.truck_id, 0.0)

    # Trucks list for package lookups
    trucks = [truck1, truck2, truck3]

    # Returns from Truck.load_packages_on_trucks as a tuple. Dissect the tuple for the information we need
    delayed_packages = Truck.load_packages_on_trucks(package_table, truck1, truck2, truck3)
    incorrect_addresses = delayed_packages[1]
   
   # Deliver packages
    truck1.packages = Truck.deliver_packages(distances, addresses, truck_table, truck1, truck1. start_time, truck1, truck2, truck3)
    truck2.packages = Truck.deliver_packages(distances, addresses, truck_table, truck2, truck2. start_time, truck1, truck2, truck3)
    truck3.packages = Truck.deliver_packages(distances, addresses, truck_table, truck3, truck3. start_time, truck1, truck2, truck3)

    # Display program
    user_interface.display(truck1, truck2, truck3, trucks, truck_table, incorrect_addresses, delayed_packages, addresses)

if __name__ == "__main__":
    main()
