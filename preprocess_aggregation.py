import argparse
import maup
import os
import geopandas

# Arguments Parsing
parser = argparse.ArgumentParser(
    description='Take in block level demographic data aggregate to precinct, and merge with election data.')
parser.add_argument("--block-demographics", help='input for block level demographic data as geojson', required=True)
parser.add_argument("--precinct-elections", help='input for precinct level election data as a geojson', required=True)
parser.add_argument("-d", help="output directory", required=True)

args = parser.parse_args()

# Make the output directory if it does not exist
if not os.path.exists(args.d):
    os.makedirs(args.d)

# Import block data, rename columns to more readable form, and remove non-relevant data
block_demographic_data = geopandas.read_file(args.block_demographics)
census_to_demographic_name_map = {"P0020001": "total_pop", "P0020002": "hispanic_pop", "P0020005": "white_pop",
                                  "P0020006": "black_pop", "P0020007": "amer_indian_pop", "P0020008": "asian_pop",
                                  "P0020009": "pacific_pop", "P0020010": "other_pop", "P0020011": "two_or_more_pop"}
block_demographic_data = block_demographic_data.rename(columns=census_to_demographic_name_map)
block_demographic_data = block_demographic_data.filter(["geometry"] + list(census_to_demographic_name_map.values()))

# Load 2020 precinct level election data and remove unnecessary data.
precinct_election_data = geopandas.read_file(args.precinct_elections)
election_type_rename_map = {"COUNTYFP": "county_fips", "NAME": "precinct_name", "G20PRERTRU": "2020_trump_votes",
                            "G20PREDBID": "2020_biden_votes"}
precinct_election_data = precinct_election_data.rename(columns=election_type_rename_map)
complete_precinct_level_data = precinct_election_data.filter(["geometry"] + list(election_type_rename_map.values()))

# Make an assignment of blocks to precinct using maup, and then use pandas groupby to aggregate data
block_to_precinct_assignment = maup.assign(block_demographic_data, complete_precinct_level_data)
columns_to_aggregate = list(block_demographic_data.columns)
columns_to_aggregate.remove("geometry")
complete_precinct_level_data[columns_to_aggregate] = block_demographic_data[columns_to_aggregate].groupby(
    block_to_precinct_assignment).sum()

# Export combined precinct level election and demographic data
complete_precinct_level_data.to_file(args.d + "\\precinct_level_elections_and_demographics.geojson", driver='GeoJSON')
