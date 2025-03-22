from datetime import datetime, timedelta
total_distance_traveled = 0.0
from HashTable import HashTable

class Truck:
    """
    Represents a delivery truck that drives at an average speed of 18mph and can hold up to 16 packages.

    Attributes:
    avg_speed (int): The average speed for all trucks is set to 18mph.
    package_capacity (int): The maximum number of packages a truck can carry, set to 16 packages.
    truck_id (int): Unique identifier for any specific truck.
    start_time (str): The truck will leave the hub at the designated start time.
    driver_id (int, optional): The ID of the driver assigned to any specific truck. 
    speed (int): The trucks speed, assigned as the average speed of 18mph.
    capacity (int): The trucks maximum capacity, initialized to be package_capacity of 16 packages.
    packages (list): Contains the packages that are currently loaded on the truck
    """

    avg_speed = 18
    package_capacity = 16

    def __init__(self, truck_id, start_time="8:20 AM", driver_id=None):
        """
        Initializes a Truck instance.

        Args:
            truck_id (int): Unique truck identiifer.
            start_time (str, optional): The start time is when the truck will leave the hub. By default, set to 8:20 AM if no time is specified upon initialization.
            driver_int(int, optional): The driver assigned to the truck. By default, No driver is assigned to a truck.

        """
        self.truck_id = truck_id
        self.start_time = start_time
        self.driver_id = driver_id
        self.speed = Truck.avg_speed
        self.capacity = Truck.package_capacity
        self.packages = []

    # Time complexity: O(1)
    # Space complexity: O(n)
    def add_package(self, package):
        """
        Adds a package to a truck if the truck capacity is not full.

        Args:
            package (Package): The package object that is being requested to be added on a truck.

        Returns:
            None
        """
        # Check if the truck has space for more packages
        if len(self.packages) < self.package_capacity:
            self.packages.append(package)
            # print(f"Package {package.package_id} added to Truck {self.truck_id}.")
        else:
            # print(f"Truck {self.truck_id} is full. Cannot add Package {package.package_id}.")
            pass

    # Time complexity: O(1)
    # Space complexity: O(1)
    def get_last_delivered_address(self):
        """
        Retrieves the address of the last delivered package.

        Returns:
            str: The address of the last delivered package
            None if no packages have been added to the truck
        """
        if self.packages:
            last_package = self.packages[-1]
            return last_package.address
        return None
    
    # Time complexity: O(n log n)
    # Space complexity: O(n)
    def load_packages_on_trucks(package_table, truck1, truck2, truck3):
        """
        Loads packages onto trucks based on delivery requirements and special considerations. See WGU Task 2 requirements for more.

        This method sorts and assigns packages based on the following:
        1. Delivery deadlines
        2. Special_note field found in Package objects
        3. Delayed packages (also in special_note field)
        4. Incorrectly addressed packages

        Args:
            package_table (HashTable): The hashtable containing information for all packages.
            truck1 (Truck): The first truck.
            truck2 (Truck): The second truck.
            truck3 (Truck): The third truck.

        Returns:
            tuple: A list containing delayed package (Package) objects, and a list containing packages (Package) that are incorrectly addressed
        """
        all_packages = package_table.get_all() # O(n)
        sorted_packages = sorted(all_packages, key=lambda x: x[0])  # Sorts packages by package id
        packages_must_be_delivered_together = []
        packages_on_specific_truck = HashTable(size=3)
        packages_on_specific_truck.insert(truck1.truck_id, [])
        packages_on_specific_truck.insert(truck2.truck_id, [])
        packages_on_specific_truck.insert(truck3.truck_id, [])
        delayed_packages = []
        delivery_by_1030 = []
        added_package_ids = set()
        incorrectly_addressed_packages = []

        # Separate packages with special notes to handle delivery requirements
        for index, (_, package) in enumerate(sorted_packages):
            if "Must be delivered with" in package.special_note:
                packages_must_be_delivered_together.append(package.package_id)
                packages_must_be_delivered_together.append(int(package.special_note[23:25]))
                packages_must_be_delivered_together.append(int(package.special_note[27:]))

            if "Can only be on" in package.special_note:
                truck_id = int(package.special_note[21:])
                packages_on_specific_truck.lookup(truck_id).append(package)

            if "Delayed" in package.special_note:
                delayed_packages.append(package)
            
            if "Wrong address" in package.special_note:
                incorrectly_addressed_packages.append(package)

            if package.delivery_deadline == "10:30 AM":
                delivery_by_1030.append(package)

        # Load packages any packages that must be delivered together on Truck 1 (Most of these have early delivery requirements, truck 1 will leave the earliest)
        # Then remove the packages from the sorted list
        for package_id in packages_must_be_delivered_together:
            package = None
            for _, p in sorted_packages:
                if p.package_id == package_id:
                    package = p
                    break
            if package and package.package_id not in added_package_ids:
                truck1.add_package(package)
                added_package_ids.add(package.package_id)
                sorted_packages = [pkg for pkg in sorted_packages if pkg[1] != package]

        # Load packages that must go on Truck 2, remove those packages from the sorted list
        for package in packages_on_specific_truck.lookup(2):
            if package.package_id not in added_package_ids:
                truck2.add_package(package)
                added_package_ids.add(package.package_id)
                sorted_packages = [pkg for pkg in sorted_packages if pkg[1] != package]

        # Load delayed packages on Truck 2 once they arrive (Truck 2 will leave in the middle of the 3 trucks, some of the delayed packages have a 10:30 delivery deadline)
        # Remove these packages from sorted list
        arrival_time = datetime.strptime("9:05 AM", "%I:%M %p")
        for dp in delayed_packages:
            if datetime.now() >= arrival_time:
                if dp.package_id not in added_package_ids:
                    truck2.add_package(dp)
                    added_package_ids.add(dp.package_id)
                    sorted_packages = [pkg for pkg in sorted_packages if pkg[1] != dp]

        # Load packages with a delivery deadline of 10:30 AM (Fill up truck 1, the remaining will go on truck 2), remove these packages from sorted list
        for package in delivery_by_1030:
            if len(truck1.packages) < 16 and package.package_id not in added_package_ids:
                truck1.add_package(package)
                added_package_ids.add(package.package_id)
                sorted_packages = [pkg for pkg in sorted_packages if pkg[1] != package]
            elif package.package_id not in added_package_ids:
                truck2.add_package(package)
                added_package_ids.add(package.package_id)
                sorted_packages = [pkg for pkg in sorted_packages if pkg[1] != package]

        # Load the remaining packages onto any available truck, remove the packages from sorted list as they're loaded
        for _, package in sorted_packages:

            if len(truck1.packages) < 16 and package.package_id not in added_package_ids:
                truck1.add_package(package)
                added_package_ids.add(package.package_id)
                sorted_packages = [pkg for pkg in sorted_packages if pkg[1] != package]
            elif len(truck3.packages) < 16 and package.package_id not in added_package_ids:
                truck3.add_package(package)
                added_package_ids.add(package.package_id)
                sorted_packages = [pkg for pkg in sorted_packages if pkg[1] != package]
            elif len(truck2.packages) < 16 and package.package_id not in added_package_ids:
                truck2.add_package(package)
                added_package_ids.add(package.package_id)
                sorted_packages = [pkg for pkg in sorted_packages if pkg[1] != package]
            else:
                print("Error: Unable to load package. All trucks are at max capacity.")


        return delayed_packages, incorrectly_addressed_packages # Check how many packages were not added (either because they were delayed or wrongly addressed)
    
     # Find distance between any two addresses
     # Time complexity: O(n) due to .index()
     # Space complexity: O(1)
    def find_distance(distances, addresses, address1, address2):
        """
        Finds the distance between two given points using a distance matrix corresponding to addresses.

        Args:
            distances [2D float matrix]: A 2D list showing the distance matrix.
            addresses (list of str): A list of addresses that correlate to the distances in the distance matrix.
            address1 (str): The starting address. (current location)
            address2 (str): The desintation address.

        Returns:
            float: The distance between the two addresses in "miles".
        """

        distance_between = distances[addresses.index(address1)][addresses.index(address2)]
        return distance_between

    # Find the minimum distance from point A -> Point B, Point B -> Point C etc. for all packages in a given truck (Greedy Nearest Neighbor)
    # Time complexity: O(n)
    # Space complexity: O(1)
    def find_min_distance(distances, addresses, from_address, truck_packages):
        """
        Finds the package with the shortest distance from the starting address 

        Args:
            distances (2D list of float): A 2D list of distances in a distance matrix.
            addresses (list of str): Addresses that correlate to the distances in the distance matrix.
            from_address (str): The starting address.
            truck_packages (list): A list of package objects on a specified truck.

        Returns:
            Package: The package object that is closest to the starting address.
        """
        min_distance = float('inf')
        nearest_package = None

        for package in truck_packages:
            package_address = package.address
            distance = Truck.find_distance(distances, addresses, from_address, package_address)

            if float(distance) < float(min_distance):
                min_distance = distance
                nearest_package = package

        return nearest_package
    
    # Time complexity: O(n log n)
    # Space complexity: O(1)
    def find_truck_id(pack_id, truck1, truck2, truck3):
        """
        Determines the truck id for any specific package.

        This function sorts the packages on each truck in order by the package id. Once sorted, a binary search algorithm is used to efficiently locate the package.

        Args:
            pack_id (int): The package ID to search for.
            truck1 (Truck): The first truck.
            truck2 (Truck): The second truck.
            truck3 (Truck): The third truck.

        Returns:
            str: A string represnetation of the truck identifier the package was located on, otherwise "Package not found on any truck" if the package was not found.
        """
        # O(n log n)
        def binary_search_for_package(truck_packages, pack_id):
            l = 0
            r = len(truck_packages) - 1
            while l <= r:
                mid = (l + r) // 2
                if truck_packages[mid].package_id == pack_id:
                    return True
                elif truck_packages[mid].package_id < pack_id:
                    l = mid + 1
                else:
                    r = mid - 1
            return False
        
            # O(n log n)
        truck1.packages.sort(key=lambda p: p.package_id)
        truck2.packages.sort(key=lambda p: p.package_id)
        truck3.packages.sort(key=lambda p: p.package_id)

        if binary_search_for_package(truck1.packages, pack_id):
            return truck1.truck_id
        if binary_search_for_package(truck2.packages, pack_id):
            return truck2.truck_id
        if binary_search_for_package(truck3.packages, pack_id):
            return truck3.truck_id

        return "Package not found on any truck."
    
    # Time complexity: O(n^2)
    # Space complexity: O(n)
    def deliver_packages(distances, addresses, truck_table, truck, start_time, truck1, truck2, truck3):
        """
        Delivers the packages on the specified truck, starting at the designated start time. The function uses a greedy nearest neighbor algorithm to determine which package to deliver next (See find_min_distance function)

        Args:
            distances (2D list of float): A 2D list of floats representing distances in a distance matrix.
            addresses (list of str): A list of addresses that correlate to the distances in the distance matrix.
            truck_table (HashTable): A hash table storing truck mileage information.
            truck (Truck): The truck object 
            start_time (str): The time the truck will "leave the hub" to start delivering packages.
            truck1 (Truck): The first truck.
            truck2 (Truck): The second truck.
            truck3 (Truck): The third truck.

        Returns:
            list: A list of packages in the order they were delivered
        """
       
        current_location = addresses[0] # WGUPS Hub
        remaining_packages = truck.packages[:] # Copy of truck.packages to alter
        delivery_order = []
        current_time = datetime.strptime(start_time, "%I:%M %p") # Converts string (time) to datetime object in the format of "xx:xx AM/PM"
        package_count = 0
        global total_distance_traveled
        
        while remaining_packages:
            nearest_package = Truck.find_min_distance(distances, addresses, current_location, remaining_packages) 
            distance = Truck.find_distance(distances, addresses, current_location, nearest_package.address)
            total_distance_traveled += float(distance)
            travel_time = timedelta(hours=(float(distance) / 18))
            current_time += travel_time
            nearest_package.delivery_time = current_time.strftime("%I:%M %p") # Converts the datetime object to a string
            nearest_package.delivery_status = "Delivered" # Update the delivery status, which reflects in the hashtable
            current_location = nearest_package.address
            delivery_order.append(nearest_package)
            truck_id = Truck.find_truck_id(nearest_package.package_id, truck1, truck2, truck3)
            if truck_id != "Package not found on any truck":
                current_truck_distance = truck_table.lookup(truck_id)
                truck_table.insert(truck_id, current_truck_distance + float(distance))
            remaining_packages.remove(nearest_package)
            package_count += 1
                
        # Account for the distance from the last package delivered back to WGUPS Hub for each truck
        distance_back_to_hub = Truck.find_distance(distances, addresses, current_location, addresses[0])
        current_truck_distance = truck_table.lookup(truck_id)
        truck_table.insert(truck_id, current_truck_distance + float(distance_back_to_hub))
        total_distance_traveled += float(distance_back_to_hub)
        return delivery_order
    
    # Time complexity: O(1)
    # Space complexity: O(1)
    def get_total_distance_traveled(truck_table):
        """
        Gets the total distance traveled by each truck and outputs the data in a formatted manner (2 decimals)

        Args:
            truck_table (HashTable): A hash table storing truck mileage information.

        Returns:
            str: A formatted string displaying the total distance traveled and the individual mileage for each truck.
        """
        global total_distance_traveled
        return "\033[1mTotal distance traveled:\033[0m {:.2f} miles".format(total_distance_traveled) + "\n\nTruck 1: {:.2f} miles".format(truck_table.lookup(1)) + "\nTruck 2: {:.2f} miles".format(truck_table.lookup(2)) + "\nTruck 3: {:.2f} miles".format(truck_table.lookup(3))
      

    # Time complexity: O(1)
    # Space complexity: O(1)
    def get_mileage(truck_table):
        """
        Generates a mileage report for all the trucks.

        Args:
            truck_table (HashTable): A hash table storing truck mileage information.

        Returns:
            str: A formatted report on the mileage of all trucks.
        """
        print("\n\033[1mMileage Report:\033[0m")
        print("=" * 170)
        return Truck.get_total_distance_traveled(truck_table) + "\n" + "=" * 170