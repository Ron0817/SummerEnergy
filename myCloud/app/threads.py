from app import app
from app.user import User, total_users
from app.__init__ import memcache
from app.config import *
import base64

import mysql.connector
#thread test
import threading
import time
from datetime import datetime

# Threads 1 monitor statistics and store into db every 5 secs
STOP = 0
def memcache_monitor():
    # Delete all rows
    query = '''DELETE FROM statistics'''
    
    cnx = mysql.connector.connect(**mysql_config)
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cnx.close()    

    duration = 5
    while not STOP:
        memcache_id = 1
        time_stamp = datetime.now().timestamp()
        time_stamp = datetime.fromtimestamp(time_stamp)
        miss_rate = 0
        hit_rate = 0
        num_of_item = len(memcache.keys())
        size = 0
        num_of_requests = 0
        
        # Insert query
        query = '''INSERT INTO `memcache`.`statistics` (`id`, `time_stamp`, `miss_rate`, `hit_rate`, `num_of_items`, `size`, `num_of_serves`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        
        cnx = mysql.connector.connect(**mysql_config)
        cursor = cnx.cursor()
        cursor.execute(query, (memcache_id, time_stamp, miss_rate, hit_rate, num_of_item, size, num_of_requests))
        cnx.commit()
        cnx.close()    
        time.sleep(duration)

        # if app.debug == True:
        #     print("FROM thread id = %s Store Time Stamp %s" % (threading.get_native_id(), time_stamp))
            


x = threading.Thread(target=memcache_monitor)
x.start()
