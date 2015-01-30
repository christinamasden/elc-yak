from api import Location, PeekLocation, Yakker
from config import GOOGLE_API_KEY, YIKYAK_USER_ID, SCHOOLS
from pygeocoder import Geocoder
import MySQLdb

def main():
    client = MySQLdb.connect("localhost","root","rtrad","yaks")
    cursor = client.cursor()
    for school in SCHOOLS:
        print 'Scraping {}'.format(school)
        location = get_location(school)
        yaks = get_yaks(location)
        for yak in yaks:
            values = (yak["messageID"], yak["message"].encode('utf-8'), str(yak["numberOfLikes"]), yak["latitude"], yak["longitude"], yak["time"])
            values2 = (str(yak["messageID"]), str(yak["numberOfLikes"]))
            cursor.execute("""REPLACE INTO yak_data(messageID, message, numberOfLikes, latitude, longitude, time) VALUES (%s, %s, %s, %s, %s, %s)""", values)
            client.commit()
            cursor.execute("""INSERT INTO like_data(messageID, numberOfLikes) VALUES (%s, %s)""", values2)
            client.commit()
    return
    client.close()

def get_location(query):
    geo_coder = Geocoder(api_key=GOOGLE_API_KEY)
    latitude , longitude = geo_coder.geocode(address=query).coordinates
    return Location(latitude, longitude)


def get_yaks(location):
    return Yakker(YIKYAK_USER_ID, location, False).get_yaks()

if __name__ == '__main__':
    main()