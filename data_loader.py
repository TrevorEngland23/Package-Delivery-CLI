from Package import Package
import csv

def load_package_data(hash_table):
    """
    Loads package data from a csv file and inserts it into a hash table.

    Args:
        hash_table (HashTable): The hash table to store package data.
    """
    with open('csv/packages.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')


        for row in reader:
            package_id = int(row[0])
            package_address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            delivery_deadline = row[5]
            weight = row[6]
            if len(row) >= 7:
                special_notes = row[7]
            else:
                special_notes = ""
        
            package = Package(package_id, package_address, city, state, zip_code, delivery_deadline, weight, "At Hub", special_notes)
            hash_table.insert(package_id, package)

def load_distance_data():
    """
    Loads distance data from a csv file and creates a distance matrix.

    Returns:
        list: 2-Dimensional list (distance matrix)
    """
    with open('csv/distances.csv', 'r') as file:
        reader = csv.reader(file)
        raw = [list(filter(None,row)) for row in reader]

        distance_matrix = []
        for i, row in enumerate(raw):
            row_val = [float(value) for value in row[: i+1]]
            distance_matrix.append(row)

        n = len(distance_matrix)
        for i in range(n):
            for j in range(i+1, n):
                distance_matrix[i].append(distance_matrix[j][i])

    return distance_matrix

def load_address_data():
    """
    Loads address data from a csv file

    Returns:
        list: A list of addresses corresponding to locations in the distance matrix.
    """
    address_data = []
    with open('csv/addresses.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            address_data.append(row[1])
    return address_data
