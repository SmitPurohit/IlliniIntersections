import sqlite3
from google.cloud import storage
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys
print('here')
mydb = mysql.connector.connect(host='34.66.84.254',
                               user='root',
                               password='illini799',
                               database='test')
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
