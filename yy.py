from api import Location, PeekLocation, Yakker
from config import GOOGLE_API_KEY, YIKYAK_USER_ID, SCHOOLS
from pygeocoder import Geocoder
from pymongo import MongoClient

def main():
    client = MongoClient()['elc']['messages']
    for school in SCHOOLS:
        print 'Scraping {}'.format(school)
        location = get_location(school)
        yaks = get_yaks(location)
        for yak in yaks:
            yak['school'] = school
            client.insert(yak)
    return

def get_location(query):
    geo_coder = Geocoder(api_key=GOOGLE_API_KEY)
    latitude , longitude = geo_coder.geocode(address=query).coordinates
    return Location(latitude, longitude)


def get_yaks(location):
    return Yakker(YIKYAK_USER_ID, location, False).get_yaks()

if __name__ == '__main__':
    main()