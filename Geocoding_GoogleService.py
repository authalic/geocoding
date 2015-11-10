
import googlemaps

# https://github.com/googlemaps/google-maps-services-python/


APIkey = "AIzaSyAOfqcW5ASoU1RgbmfuuV_-NJVWuI_MlKU"

gmaps = googlemaps.Client(key=APIkey)

gcode = gmaps.geocode('6550 S Millrock Dr, Salt Lake City, UT')

# gcode is a list, containing 1 dictonary per geocoding result
# 1 address may return more than 1 result, but the first one is usually the best.

print gcode

