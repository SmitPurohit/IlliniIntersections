import sqlite3
from google.cloud import storage
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys


def authenticate():
    with open('./config.txt', 'r') as f:
        HOST = f.readline().strip()
        USER = f.readline().strip()
        PASSWORD = f.readline().strip()
        DATABASE = f.readline().strip()

    mydb = mysql.connector.connect(host=HOST,
                                   user=USER,
                                   password=PASSWORD,
                                   database=DATABASE)
    return mydb

# return the intersection info for these two streets
def get_intersection_info(ew_name, ns_name):
    database = authenticate()
    # Returns streetID
    streetEW_q = (f"SELECT streetid "
                 f"FROM Street "
                 f"WHERE name = '{ew_name}'")
    # Returns streetID
    streetNS_q = (f"SELECT streetid " 
                 f"FROM Street "
                 f"WHERE name = '{ns_name}'")

    intersectionID_q = (f"SELECT intersectionID "
                 f"FROM Intersection "
                 f"WHERE streetEWID = ({streetEW_q}) AND streetNSID = ({streetNS_q})")

    intersectionData_q = (f"SELECT intersectionID, comments, overallRating, visualAppeal "
                        f"FROM Intersection NATURAL JOIN Reviews "
                        f"WHERE intersectionID = ({intersectionID_q})")


    cursor = database.cursor()
    cursor.execute(intersectionData_q)
    result = cursor.fetchall()
    for x in result:
        print(x)
    intersectionID, comments, overallRating, visualAppeal = result[0]
    return intersectionID, comments, overallRating, visualAppeal



def advanced_queries(database):
    subquery1 = ("SELECT streetEWID "
                 "FROM Statistics s JOIN Intersection i on s.statisticsID = i.intersectionID "
                 "WHERE lightingRating >= 8.0")
    subquery2 = ("SELECT streetNSID "
                 "FROM Statistics s JOIN Intersection i on s.statisticsID = i.intersectionID "
                 "WHERE lightingRating >= 8.0")

    cursor = database.cursor()
    cursor.execute(
        f"SELECT name, direction FROM Street "
        f"WHERE streetID IN ({subquery1} UNION {subquery2}) "
        f"GROUP BY name, direction "
        f"LIMIT 15; "
    )
    result = cursor.fetchall()
    for x in result:
        print(x)
