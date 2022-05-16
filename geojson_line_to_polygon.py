import argparse
import geopandas
from shapely.geometry import Polygon

# Arguments Parsing
parser = argparse.ArgumentParser(
    description='Take in district shape data as geojson, and map precinct data to districts with an ID')
parser.add_argument("-i", help="input file", required=True)
parser.add_argument("-d", help="output file", required=True)
args = parser.parse_args()

geojson = geopandas.read_file(args.i)

d = {'geometry': []}

for i in range(len(geojson.geometry)):
    # print(geojson)
    # d['name'].append(geojson.name[i])
    d['geometry'].append(Polygon(geojson.geometry[i].coords))

# print(d)

new_geojson = geopandas.GeoDataFrame(d)
new_geojson.to_file(args.d, driver='GeoJSON')
print('wrote to', args.d)