import sqlite3
from google.cloud import storage
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys
with open('config.txt', 'r') as f:
    HOST = f.readline().strip()
    USER = f.readline().strip()
    PASSWORD = f.readline().strip()
    DATABASE = f.readline().strip()

mydb = mysql.connector.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               database=DATABASE)
print('here2')
subquery1 = ("SELECT streetEWID FROM Statistics s JOIN Intersection i on s.statisticsID = i.intersectionID WHERE lightingRating >= 8.0")
subquery2 = ("SELECT streetNSID FROM Statistics s JOIN Intersection i on s.statisticsID = i.intersectionID WHERE lightingRating >= 8.0")

cursor = mydb.cursor()
cursor.execute(
    f"SELECT name, direction FROM Street "
    f"WHERE streetID IN ({subquery1} UNION {subquery2}) "
    f"GROUP BY name, direction "
    f"LIMIT 15; "
)
result = cursor.fetchall()
print('Length of Result: {}'.format(len(result)))
for x in result:
    print(x)
