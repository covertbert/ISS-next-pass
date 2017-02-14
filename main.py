import urllib2
import json
from datetime import datetime
from geopy.geocoders import Nominatim
import time

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


def output_date(iss_date):
    """ Takes the ISS date object as a parameter and determines if that date is today or tomorrow or other"""

    # Assign basic ISS date variables
    iss_next_pass_full_date = iss_date.strftime('%Y-%m-%d')
    iss_next_pass_year_month = iss_date.strftime('%Y-%m')
    iss_next_pass_day = iss_date.strftime('%d')

    # Assign basic today's date variables
    today_full_date = time.strftime('%Y-%m-%d')
    today_year_month = time.strftime('%Y-%m')
    today_day = time.strftime('%d')

    # Split ISS date object into component parts from string building
    day = iss_date.strftime('%d')
    month = iss_date.strftime('%m')
    year = iss_date.strftime('%Y')
    the_time = iss_date.strftime('%H:%M:%S')

    # If date is today return today. If date is tomorrow, return tomorrow. Else return False
    if iss_next_pass_full_date == today_full_date:
        return 'today at %s' % the_time
    elif iss_next_pass_year_month == today_year_month and int(iss_next_pass_day) == int(today_day) + 1:
        return 'tomorrow at %s' % the_time
    else:
        return 'on %s/%s/%s at %s' % (day, month, year, the_time)


def init():
    """ Initialises most of the things"""

    # Assign rise data
    iss_data = get_iss_rise_time()
    address = iss_data[0]
    date_time = datetime.fromtimestamp(iss_data[1])

    # Create date object from data
    datetime_object = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S')

    # Print the output to the command line
    print 'The ISS will next pass over %s %s' % (address, output_date(datetime_object))

init()
