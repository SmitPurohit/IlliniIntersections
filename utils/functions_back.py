import sqlite3
from google.cloud import storage
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys
import requests

GAK = 'AIzaSyARw7vsFpe6UKaUMAAkAngIVdmFBjDxIfY'


# Logs into GCP through secure log in
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

# Advanced query 1
def runQuery1():
    database = authenticate()
    query1 = ("SELECT name, direction FROM Street WHERE streetID in ((SELECT streetEWID FROM Statistics s JOIN Intersection i on s.statisticsID = i.intersectionID WHERE lightingRating >= 8.0) UNION (SELECT streetNSID FROM Statistics s JOIN Intersection i on s.statisticsID = i.intersectionID WHERE lightingRating >= 8.0)) GROUP BY name, direction")


    cursor = database.cursor()
    cursor.execute(query1)
    result = cursor.fetchall()
    return result

# Advanced query 2
def runQuery2():
    database = authenticate()
    query1 = ("SELECT r.intersectionID, ABS(r.qualityRating - s.roadQuality) AS Difference, AVG(r.overallRating) AS AverageOverallRating FROM Reviews r JOIN Statistics s on r.intersectionID = s.statisticsID WHERE intersectionID in ( SELECT r.intersectionID FROM Reviews r JOIN Statistics s on r.intersectionID = s.statisticsID WHERE ABS(r.qualityRating - s.roadQuality) <= 1.0) GROUP BY r.intersectionID, Difference ORDER BY Difference")


    cursor = database.cursor()
    cursor.execute(query1)
    result = cursor.fetchall()
    return result


# Retrieves and displays statistics of an intersection given its two street names.
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

    intersectionData_q = (f"SELECT intersectionID, comments, overallRating, visualAppeal, lightingRating, qualityRating, trafficRating, views "
                        f"FROM Intersection NATURAL JOIN Reviews "
                        f"WHERE intersectionID = ({intersectionID_q})")


    cursor = database.cursor()
    cursor.execute(intersectionData_q)
    result = cursor.fetchall()
    for x in result:
        print(x)
    intersectionID, comments, overallRating, visualAppeal, lightingRating, qualityRating, trafficRating, views= result[0]
    return intersectionID, comments, overallRating, visualAppeal, lightingRating, qualityRating, trafficRating, views


# Inserts a review into the database.
def insert_review(intersection_id, lighting, road_quality, traffic, visual_appeal, comments):
    database = authenticate()
    username = 'adam85'

    overall_rating = round((int(lighting) + int(road_quality) + int(traffic) + int(visual_appeal)) / 4)

    review_number_q = ("SELECT MAX(reviewNumber) FROM Reviews")
    cursor = database.cursor()
    cursor.execute(review_number_q)
    result = cursor.fetchall()
    review_number = (result[0][0]) + 1



    # Used IntersectionID 5999 for testing.

    insertion_query = (f"INSERT INTO Reviews "
                       f"VALUES({review_number}, {intersection_id}, '{comments}',"
                       f"{overall_rating}, {lighting}, {road_quality}, {traffic},"
                       f"{visual_appeal}, '{username}')")
    cursor = database.cursor()
    cursor.execute(insertion_query)
    database.commit()
    cursor.close()
    database.close()


# Updates a review within the database.
def update_review(review_number, comment):
    database = authenticate()

    update_query = (f"UPDATE Reviews SET "
                    f"comments = '{comment}' "
                    f"WHERE reviewNumber = {review_number}")
    search_query = (f"SELECT * FROM Reviews WHERE reviewNumber = {review_number}")
    cursor = database.cursor()
    cursor.execute(search_query)
    oldResult = cursor.fetchall()
    cursor.execute(update_query)
    cursor.execute(search_query)
    newResult = cursor.fetchall()
    database.commit()
    cursor.close()
    database.close()
    return oldResult, newResult


# Deletes a review within the database.
def delete_review(review_number):
    database = authenticate()
    print(review_number)
    delete_query = (f"DELETE FROM Reviews WHERE reviewNumber = {review_number}")
    cursor = database.cursor()
    cursor.execute(delete_query)
    database.commit()
    database.close()

def user_auth(username, password):
    database = authenticate()
    auth_query = (f"SELECT * FROM User WHERE username = '{username}' and password = '{password}'")
    cursor = database.cursor()
    cursor.execute(auth_query)
    row = cursor.fetchone()
    if row == None:
        database.close()
        return 0
    else:
        database.close()   
        return 1
    

def user_signup(username,firstName,lastName,password):
    database = authenticate()
    auth_query = (f"SELECT * FROM User WHERE username = '{username}'")
    sign_query = (f"INSERT INTO User (username,firstName,lastName,password) VALUES('{username}','{firstName}','{lastName}','{password}')")
    cursor = database.cursor()
    cursor.execute(auth_query)
    row = cursor.fetchone()
    if row == None:
        cursor = database.cursor()
        cursor.execute(sign_query)
        database.commit()
        database.close()
        return 0
    else:
        database.close()   
        return 1
def geocode(address):
    lat, lng = None, None
    api_key = GAK
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={api_key}"
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return lat, lng

    







