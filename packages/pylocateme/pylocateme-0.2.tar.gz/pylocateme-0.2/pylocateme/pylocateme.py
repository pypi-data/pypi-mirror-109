from geopy.geocoders import Nominatim
import time
from pprint import pprint
def pylocateme(place,country):
    location = Nominatim(user_agent="tutorial")
    location1 = location.geocode(str(place)+","+str(country)).raw
    pprint(location1)
pl = input("Enter place: ")
cn = input("Enter country: ")
pylocateme(pl,cn)
