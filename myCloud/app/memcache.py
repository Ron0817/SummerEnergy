class Memcache:
    def __init__(self):
        self.cache = {}

    def put(self, key, value):
        self.cache.update({key: value})

    def get(self, key):    
        value = self.cache.get(key)
        return value

    def clear(self):
        self.cache.clear()

    def invalidate_key(self, key):
        self.cache.pop(key)
    
    def values(self):
        return self.cache.values()

    def keys(self):
        return self.cache.keys()
    
    def items(self):
        return self.cache.items()
    
    def itself(self):
        return self.cache