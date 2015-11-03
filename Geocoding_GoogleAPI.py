#Geocode a list of addresses using Google Maps API v3
#usage limit:  2500 addresses per day

#Geocoding API Documentation -- https://developers.google.com/maps/documentation/geocoding/intro
#Client Lib -- https://github.com/googlemaps/google-maps-services-python/


import urllib
import xml.etree.ElementTree as xml


APIkey = "AIzaSyAOfqcW5ASoU1RgbmfuuV_-NJVWuI_MlKU"
# documentation 

# Define the locations of the input and output text files

# Input file must be a text file of formatted addresses of the type that can be entered in a
#  Google Maps search window
# Output file will be created, or overwritten if already exists.

inputfile = r'C:\projects\geocoding\addresses.txt'
outputfile = r'C:\projects\geocoding\output.txt'


# XML processing function

def ParseXML(XMLfile):
    '''Accepts an XML file. Returns a tab-delimited line of text containing results of geocoding'''
    fullAddr = ""
    status = ""
    locType = ""
    lat = ""
    lon = ""
    
    # parse the XML string into a tree of Elements
    tree = xml.parse(XMLfile)
        
    # get the root element of the tree
    rootElem = tree.getroot()
    
    # get the Status element, under the root
    statusElem = rootElem.find("status")
    
    # get the text contents of the Status element
    status = statusElem.text
    
    # get the result element, under the root
    resultElem = rootElem.find("result")
    
    # get the formatted address element returned from the API
    formAddElem = resultElem.find("formatted_address")
    
    # get the formatted address string from the element
    fullAddr = formAddElem.text
    
    # get the geometry element under the result element
    geomElem = resultElem.find("geometry")
    
    # get the location element from the geometry element
    locElem = geomElem.find("location")
    
    # get the Lat and Lon elements from location element
    latElem = locElem.find("lat")
    lonElem = locElem.find("lng")
    
    # get the lat and lon values from the Lat and Lon elements
    lat = latElem.text
    lon = lonElem.text
    
    # get the location type element from the geometry element
    locTypeElem = geomElem.find("location_type")
    
    # get the location type string from the element
    locType = locTypeElem.text

    return "%s\t%s\t%s\t%s\t%s\n" % (fullAddr, status, locType, lat, lon)




input = open(inputfile, 'r')
output = open(outputfile, 'w')

inputlines = input.readlines()

# write field name header of output file
outputheader = "FORMATTEDADDR\tSTATUS\tLOCTYPE\tLAT\tLON\n"
output.write(outputheader)

# loop through the input addresses
for line in inputlines:
    address = urllib.quote_plus(line)
    
    url = "http://maps.googleapis.com/maps/api/geocode/xml?address=%s&sensor=false" % (address)
    
    print line

    # get result from Geocoder
    result = urllib.urlopen(url)
    
    try:
        outline = ParseXML(result)
    except AttributeError:
        # AttributeError pops up occasionally:
        #    'NoneType' object has no attribute 'find'
        # Return the address with no geocoding information and continue
        outline = line

    output.write(outline)
    
    result.close()

print "done"

output.close()
