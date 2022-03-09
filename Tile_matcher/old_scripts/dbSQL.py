# Tutorial
# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
# https://www.youtube.com/watch?v=byHcYRpMgI4

import sqlite3
from sqlite3 import Error
import numpy as np
import math
import matplotlib.pyplot as plt
import struct
import os
import sys

### DATA TYPE
# NULL
# INTEGER
# REAL
# TEXT
# BLOB

### SET THE DATABASE PATH
db_path = 'C:/Users/Luscias/Desktop/3DOM/07_LFNet/provaGCP/db.db'


"""
conn = sqlite3.connect(db_path) # Connect to the database
c = conn.cursor() # Create a cursor
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())
conn.commit() # Commit our command  
conn.close() # Close our connection
#"""

"""
conn = sqlite3.connect(db_path) # Connect to the database
c = conn.cursor() # Create a cursor
c.execute("SELECT * FROM sqlite_sequence")
items = c.fetchall()
print(len(items))
print(items)
conn.commit() # Commit our command  
conn.close() # Close our connection
#"""

#"""
conn = sqlite3.connect(db_path) # Connect to the database
c = conn.cursor() # Create a cursor
c.execute("SELECT * FROM descriptors")
items = c.fetchone()
print(items[0])
print(items[1])
print(items[2])
print(type(items[3]))
print(sys.getsizeof(items[3]))
print((sys.getsizeof(items[3])/128-8002)*128)
conn.commit() # Commit our command  
conn.close() # Close our connection
#"""


print("unpack :")

print(struct.unpack('1024323B', items[3]))















## Create a table
#c.execute(""" CREATE TABLE customers (
#        first_name text,
#        last_name text,
#        email text
#        )""")

## Fill the table
#c.execute(" INSERT INTO customers VALUES ('L', 'M', 'lm@codemy.com')")

### Fill the table
#many_customers = [
#                    ('Alby','Furlani','alby@furlani'),
#                    ('Gabry','Righetti','gabry@rughetti'),
#                    ('bla','blabla','bla@blabla'),
#                    ]
#
#c.executemany("INSERT INTO customers VALUES (?,?,?)", many_customers)

#c.execute("SELECT rowid, * FROM customers")
#print(c.fetchone())
#print(c.fetchmany(3))
#print(c.fetchall())
#items = c.fetchall()

#for item in items:
#    print(item[0] + " " + item[1])
#for item in items:
#    print(item)





