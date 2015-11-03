# Geocode a list of addresses using Google Maps API v3
# usage limit:  2500 addresses per day

# Geocoding API Documentation -- https://developers.google.com/maps/documentation/geocoding/intro
# Client Lib -- https://github.com/googlemaps/google-maps-services-python/

import urllib
import json

APIkey = "AIzaSyAOfqcW5ASoU1RgbmfuuV_-NJVWuI_MlKU"

# Input file must be a text file of formatted addresses of the type that can be entered in a Google Maps search window
# Output file will be created, or overwritten if already exists.

inputfile = r'C:\projects\geocoding\addresses.txt'
outputfile = r'C:\projects\geocoding\output.txt'

# JSON processing function
def ParseJSON(JSONfile):
    '''Accepts a JSON file. Returns a tab-delimited line of text containing results of geocoding'''

    resultJSON = json.loads(JSONfile)

    fullAddr = resultJSON['results'][0]['formatted_address']
    status = resultJSON['status']
    locType = resultJSON['results'][0]['geometry']['location_type']
    lat = resultJSON['results'][0]['geometry']['location']['lat']
    lon = resultJSON['results'][0]['geometry']['location']['lng']

    return "%s\t%s\t%s\t%s\t%s\n" % (fullAddr, status, locType, lat, lon)

input = open(inputfile, 'r')
output = open(outputfile, 'w')

inputlines = input.readlines()
input.close()

# write field name header of output file
outputheader = "FORMATTEDADDR\tSTATUS\tLOCTYPE\tLAT\tLON\n"
output.write(outputheader)

# loop through the input addresses
for line in inputlines:
    # format the address to be friendly as a URL parameter
    address = urllib.quote_plus(line)
    
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address, APIkey)

    print line[:-1]
    print url + '\n'

    try:
        # get result from Geocoder
        result = urllib.urlopen(url).read()
        outline = ParseJSON(result)
        output.write(outline)
    except IOError:
        outline = "Google Service Error:  Timed out\n"
        print outline
        output.write(outline)

print "done"

output.close()
