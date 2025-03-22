from datetime import datetime
from Truck import Truck

class Package:
    """
        Represents a delivery package.

        Attributes:
            package_id (int): Unique identifier for a specific package.
            address (str): The delivery address of the package.
            city (str): The city of the delivery address.
            state (str): The state of the delivery address.
            zip_code (str): The zip code of the delivery address.
            delivery_deadline (str): The package must be delivered by this time.
            weight (float): The weight of the package.
            delivery_status (str): The current delivery status of the package.
            special_note (str, optional): If available, represents additional requirements for the package.
            delivery_time (str, optional): The time the package is delivered, originally set to None
        """
    
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight, delivery_status, special_note=""):
        """
        Initializes a Package instance with the following information.

        Args:
            package_id (int): Unique identifier for the package.
            address (str): The delivery address of the package.
            city (str): The city of the delivery address.
            state (str): The state of the delivery address.
            zip_code (str): The zip code of the delivery address.
            delivery_deadline (str): The package must be delivered by this time.
            weight (float): The weight of the package.
            delivery_status (str): The current delivery status of the package.
            special_note (str, optional): If available, represents additional requirements for the package.
            delivery_time (str, optional): The time the package is delivered, originally set to None
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.delivery_status = delivery_status
        self.special_note = special_note
        self.delivery_time = None
       

    def __str__(self):
        """
        Returns a formatted string representation of the package details.

        Returns:
            str: A custom string containing the packages details.
        """
        return ("Package {}: {}, {}, {} {} | Deadline: {} | Weight: {} | Status: {} | Delivery Time: {} | Notes: {}".format(self.package_id, self.address, self.city, self.state, self.zip_code, self.delivery_deadline, self.weight, self.delivery_status, self.delivery_time,self.special_note))
        
    def __repr__(self):
        """
        Returns an offical string representation of the package.

        Returns:
            str: A string representation of the package instance.
        """
        return self.__str__() 
      
    # Time complexity: O(n)
    # Space complexity: O(1)
    def change_package_address(incorrect_addresses_list, specified_time):
        """
        Updates the address of packages in the incorrect packages list at a specified time

        Params:
            incorrect_addresses_list (list): A list of package objects with an incorrect delivery address
            specified_time (str): The time that determines when a package address can be updated

        Returns:
            list: The list of incorrect packages with newly updated addresses.
        """
        address_correction_time = datetime.strptime("10:20 AM", "%I:%M %p")
            
        for package in incorrect_addresses_list:
            if specified_time >= address_correction_time:
                    
                # Package 9
                package.address = "410 S State St"
                package.city = "Salt Lake City"
                package.state = "UT"
                package.zip_code = "84111"
                
            else:
                # Boo this
                if specified_time < address_correction_time:
                    package.address = "300 State St"
                    package.city = "Salt Lake City"
                    package.state = "UT"
                    package.zip_code = "84103"
        return incorrect_addresses_list
    
    # Time complexity: O(t * p)
    # Space complexity: O(1)
    def get_package_status(package_id, specified_time, truck1, truck2, truck3, trucks, incorrect_addresses, delayed_packages, addresses):
            """
            Retrieves the current status for a specified package at a specified time.

            Args: 
                package_id (int): The unique identifier for the package to view the package status.
                specified_time (str): The time in which to check the package's status (Example: Check package id 9 at 10:00 AM to see the package's status at that time.)
                truck1 (Truck): The first truck.
                truck2 (Truck): The second truck.
                truck3 (Truck): The third truck.
                trucks (list): A list of Truck objects with packages on the respective truck.
                incorrect_address (list): A list of package objects that have an incorrect delivery address.
                delayed_packages (list): A list of package objects that have been identified as delayed packages.
                addresses (list): A list of addresses pertaining to the package objects.

            Returns:
            str: A formatted string displaying the package status and details in the user interface. Otherwise, a message stating the package cannot be found.
            """

            specified_time = datetime.strptime(specified_time, "%I:%M %p")
            

            for truck in trucks:
                for package in truck.packages:
                    if package.package_id == package_id:
                        truck_id = Truck.find_truck_id(package_id, truck1, truck2, truck3) # Binary search to find which truck the package is on
                        incorrect_packages = Package.change_package_address(incorrect_addresses, specified_time)
                        if specified_time >= datetime.strptime("10:20 AM", "%I:%M %p"): # If the query time is 10:20 AM or after, package updates should be shown and reflected
                            if package in incorrect_packages:
                                print("Package Updates: \n")
                                print("({}): Address Update for Package {}".format(datetime.strptime("10:20 AM", "%I:%M %p").time(), package.package_id))
                                print("New Address: {}, {}, {} {}".format(package.address, package.city, package.state, package.zip_code) + "\n" + "=" * 170 + "\n") 
                                    
                        if package.delivery_time:
                            if specified_time >= datetime.strptime(package.delivery_time, "%I:%M %p"):
                                package.delivery_status = "Delivered"
                                return "({}): Package {} status: {} by Truck {} at {} to {}".format(specified_time.time(), package.package_id, package.delivery_status, truck_id, package.delivery_time, package.address) + " \n" + "=" * 170
                        
                            if specified_time >= datetime.strptime(truck.start_time, "%I:%M %p"):
                                package.delivery_status = "Out For Delivery"
                                return "({}): Package {} status: {} by Truck {} to {}".format(specified_time.time(), package.package_id, package.delivery_status, truck_id, package.address) + " \n" + "=" * 170
                                    
                            if package not in delayed_packages[0]:
                                package.delivery_status = "At WGUPS Hub (" + addresses[0] +")"
                                return "({}): Package {} status: {} assigned to Truck {}. Truck {}'s scheduled start time: {}. Scheduled delivery location: {}".format(specified_time.time(), package.package_id, package.delivery_status, truck_id, truck_id, truck.start_time, package.address) + " \n" + "=" * 170
                            else:
                                if specified_time < datetime.strptime("9:05 AM", "%I:%M %p"):
                                    package.delivery_status = "Delayed - Arriving to WGUPS Hub at 9:05 AM"
                                    return "({}): Package {} status: {}. Scheduled delivery location: {}".format(specified_time.time(), package.package_id, package.delivery_status, package.address) + " \n" + "=" * 170
                                elif specified_time < datetime.strptime(truck.start_time, "%I:%M %p") and specified_time >= datetime.strptime("9:05 AM", "%I:%M %p"):
                                    package.delivery_status = "At WGUPS Hub (" + addresses[0] +")"
                                    return "({}): Package {} status: {} assigned to Truck {}. Truck {}'s scheduled start time: {}. Scheduled delivery location: {}".format(specified_time.time(), package.package_id, package.delivery_status, truck_id, truck_id, truck.start_time, package.address) + " \n" + "=" * 170
                                elif specified_time >= datetime.strptime(truck.start_time, "%I:%M %p"):
                                    package.delivery_status = "Out For Delivery"
                                    return "({}): Package {} status: {} by Truck {} to {}".format(specified_time.time(), package.package_id, package.delivery_status, truck_id, package.address) + " \n" + "=" * 170
                                elif specified_time >= datetime.strptime(package.delivery_time, "%I:%M %p"):
                                    package.delivery_status = "Delivered"
                                    return "({}): Package {} status: {} by Truck {} at {} to {}".format(specified_time.time(), package.package_id, package.delivery_status, truck_id, package.delivery_time, package.address) + " \n" + "=" * 170
            
            return "({}): Status: Package not found.".format(specified_time) + " \n" + "=" * 170
    
    # Time complexity: O(t * p)
    # Space complexity: O(1)
    def package_status_summary(trucks):
        """
        Generates a summary report on the delivery status for each truck.

        Args:
            trucks (list): A list of Truck objects containing packages to be delivered
            
        Prints:
            - The number of delivered packages per truck.
            - The number of packages yet to be delivered per truck.
        """
        print("Delivery Summary: \n")
        for truck in trucks:
            delivery_count = 0
            pending_delivery = len(truck.packages)
            for package in truck.packages:
                
                if package.delivery_status == "Delivered":
                    delivery_count += 1
                    pending_delivery -= 1
                
            print("Truck {}: Delivered - {} | Pending: {} ".format(truck.truck_id, delivery_count, pending_delivery))
        print ("=" * 170 + "\n")

    # Time complexity: O(t * p)
    # Space complexity: O(t * p)
    def get_all_package_status(specified_time, truck1, truck2, truck3, trucks, incorrect_addresses, delayed_packages, addresses):
        """
        Gets the package status for all packages at the specified time.

        Args:
            specified_time (str): The time to check the status of all packages.
            truck1 (Truck): The first truck.
            truck2 (Truck): The second truck.
            truck3 (Truck): The third truck.
            trucks (list): A list of Truck objects with packages on the respective truck.
            incorrect_address (list): A list of package objects that have an incorrect delivery address.
            delayed_packages (list): A list of package objects that have been identified as delayed packages.
            addresses (list): A list of addresses pertaining to the package objects.

        Returns:
            str: A formatted string displaying the status of all packages at the specified time.
        """

        print("\n\033[1mAll Packages Status Report By Time:\033[0m")
        print("=" * 170, end=None)
            
        status_report = []  # Store status messages

        for truck in trucks:
            for package in truck.packages:
                package_status = Package.get_package_status(package.package_id, specified_time, truck1, truck2, truck3, trucks, incorrect_addresses, delayed_packages, addresses)
                status_report.append(package_status)
        Package.package_status_summary(trucks)

        specified_time = datetime.strptime(specified_time, "%I:%M %p")

        return "\n".join(status_report)