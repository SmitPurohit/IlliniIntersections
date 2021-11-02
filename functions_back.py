import sqlite3
from google.cloud import storage
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys
print('here')
mydb = mysql.connector.connect(host='34.66.84.254', user='root', password='illini799', database='test')
print('here2')
cursor = mydb.cursor()
cursor.execute("SELECT * FROM User")
result = cursor.fetchall()
print('Length of Result: {}'.format(len(result)))
for x in result:
    print(x)
