class HashTable:
    """
    A hash table using chaining for collision resolution.
    """
    def __init__(self, size=40):
        """
        Initializes the hash table with a fixed size of 40 items.
        Each index in the hash table is initialized to None (Just to create the table)
        """
        self.size = size
        self.table = [None] * self.size

    def __getitem__(self, key):
        return self.table

    def get_hash(self, key):
        """
        Computes a hash for the key.

        Args:
            key (str): The key that will be hashed

        Returns:
            int: The index position in the hash talbe where the key-value pair is stored.
        """
        hash = 0
        for c in str(key):
            hash += ord(c) # Adds ASCII value of each character of the key to the hash
            return hash % self.size
        
    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash table

        If the key already exists, the value of the key is updated.

        Args:
            key (str): The key associated with the value
            value (any): The value of the key

        Returns:
            bool: True if the insertion completes, False if the insertion does not complete.
        """
        key_hash = self.get_hash(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True
        
    def lookup(self, key):
        """
        Retrieves a value from the hash table using the given key (id)

        Args:
            key (str): The key to obtain the key's values.
        
        Returns:
            any: The value associated with the key (Package)
            None if the key is not found.
        """
        key_hash = self.get_hash(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
                
        return None
    
    def get_all(self):
        """
        Retrieves all key-value pairs stored in the hash table.

        Returns:
            list: A list of all key-value pairs stored in the hash table.
        """
        all = []
        for bucket in self.table:
            if bucket is not None:
                for item in bucket:
                    all.append(item)
        return all
    

    def delete(self, key):
        """
        Deletes a key-value pair from the hash table.

        Args:
            key (str): The key to be removed.

        Returns:
            bool: True if the key is successfully removed, False if the key is not found/cannot be removed.
        """
        key_hash = self.get_hash(key)

        if self.table[key_hash] is None:
            return False

        for i in range(0, len(self.table[key_hash])):
            if self.table[key_hash][i][0] == key:
                self.table[key_hash].pop(i)
                return True
        return False
    
