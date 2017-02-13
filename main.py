import urllib2
import json
from datetime import datetime
from geopy.geocoders import Nominatim

GEO_LOCATOR = Nominatim()


def address_input():
    """ Prompts for an address and returns it """
    return raw_input('Enter your address: ')


def build_location_array():
    """ Builds an array of data containing lat and long and returns it """

    # Gets location data based on input
    location_data = GEO_LOCATOR.geocode(address_input())

    return [location_data.address, location_data.latitude, location_data.longitude]


def get_iss_rise_time():
    """ Takes location data, queries ISS Api for next pass data and returns it"""

    # Assigning the location data to variables for later use
    location_data = build_location_array()
    address = location_data[0]
    latitude = location_data[1]
    longitude = location_data[2]

    # API request and handling of location data
    api_request = 'http://api.open-notify.org/iss-pass.json?lat=%s&lon=%s&alt=20&n=20' % (latitude, longitude)
    response = urllib2.urlopen(api_request)
    iss_pass_object = json.loads(response.read())
    next_rise_timestamp = iss_pass_object['response'][0]['risetime']

    return [address, next_rise_timestamp]


def output_iss_rise_data():
    """ Takes next-rise time stamp, converts it to human readable and prints"""

    # Assign rise data
    iss_data = get_iss_rise_time()
    address = iss_data[0]
    date_time = datetime.fromtimestamp(iss_data[1])

    # Create date object from data
    datetime_object = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S')

    # Split date object into component parts from string building
    day = datetime_object.strftime('%d')
    month = datetime_object.strftime('%m')
    year = datetime_object.strftime('%Y')
    time = datetime_object.strftime('%H:%M:%S')

    print 'The ISS will next pass over %s on %s/%s/%s at %s' % (address, day, month, year, time)

output_iss_rise_data()
