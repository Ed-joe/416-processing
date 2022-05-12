import maup
import argparse
import geopandas

# Arguments Parsing
parser = argparse.ArgumentParser(
    description='Take in district shape data as geojson, and map precinct data to districts with an ID')
parser.add_argument("--precinct-shape", help='precinct shape data', required=True)
parser.add_argument("--district-shape", help='precinct shape data', required=True)
parser.add_argument("-d", help="output directory", required=True)
args = parser.parse_args()

precincts = geopandas.read_file(args.precinct_shape)
districts = geopandas.read_file(args.district_shape)

assignment = maup.assign(precincts, districts)

# # Add the assigned districts as a column of the `precincts` GeoDataFrame:
# precincts["mapping"] = assignment

# Save a separate mapping
assignment.to_csv(args.d + "\\mapping.csv")

# # Save updated geodataframe
# precincts.to_file(args.d + "\\precinct_level_elections_and_demographics_with_map.geojson", driver='GeoJSON')
