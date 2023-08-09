import mysql.connector
from app.config import mysql_config

class Memcache:
    def __init__(self, capacity, replacement_policy):
        self.cache = {}
        self.replacement_policy = replacement_policy
        self.capacity = capacity
        self.num_of_serve = 0
        self.miss_rate = 0
        self.hit_rate = 0        

    def values(self):
        return self.cache.values()

    def keys(self):
        return self.cache.keys()
    
    def items(self):
        return self.cache.items()
    
    def itself(self):
        return self.cache
    
    def put(self, key, value):
        self.cache.update({key: value})

    def get(self, key):    
        value = self.cache.get(key)
        return value

    def clear(self):
        self.cache.clear()

    def invalidate_key(self, key):
        self.cache.pop(key)
    
    def refresh_configuration(self):
        # Read from rd
        query = "SELECT * FROM config WHERE id=1"
        cnx = mysql.connector.connect(**mysql_config)
        cursor = cnx.cursor()
        cursor.execute(query)
        for row in cursor:
            # Only base on the first row
            if int(row[0]) == 1:
                policy = str(row[1])
                capacity = float(row[2])
        cnx.close()    
        # Update memcache params
        self.replacement_policy = policy
        self.capacity = capacity
        return 0
    
