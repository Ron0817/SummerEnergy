import mysql.connector
import random
import sys
from app.config import mysql_config

class Memcache:
    def __init__(self, capacity, replacement_policy):
        self.cache = {}
        # policy {Random, RR}
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
    
    def getsize(self):
        return sys.getsizeof(self.cache)
    
    def put(self, key, value):
        print("MEMCACHE size now is %s NEW IMAGE size now is %s CAPACITY is %s" % (sys.getsizeof(self.cache), sys.getsizeof(value), self.capacity * 1024))
        # If new size > maximum capacity of cache; then call replace_policy 
        if sys.getsizeof(self.cache) > self.capacity * 9999:    # No use temporarily
            if len(self.cache.keys()) >= 1:
                replaced_idx = self.replace_by_policy(key, value)
            else:
                self.cache.update({key: value})    
                replaced_idx = 0
        else:    
            self.cache.update({key: value})
            replaced_idx = 0
        return replaced_idx

    def get(self, key):    
        value = self.cache.get(key)
        return value

    def clear(self):
        self.cache.clear()

    def invalidate_key(self, key):
        self.cache.pop(key)
    
    def refresh_configuration(self):
        # Read from memcache.config.firstline
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
    
    def replace_by_policy(self, key,value):
        # Only being supported in Python 3.10 +
        match self.replacement_policy:
            case "Random":
                random_idx = random.sample(self.cache.keys(), 1)[0]
                self.cache.pop(random_idx)
                self.cache.update({key: value})
                return random_idx
            
            case "RR":
                print("placeholder for RR policy")
                return 0

            case _:
                random_idx = random.sample(self.cache.keys(), 1)[0]
                self.cache.update({random_idx: value})
                return random_idx


    
