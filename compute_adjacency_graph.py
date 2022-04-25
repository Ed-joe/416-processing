from gerrychain import Graph
import os
import geopandas as gpd
import argparse

#Arguments Parsing
parser = argparse.ArgumentParser(description='Take in precinct geojson with election and demographic information')
parser.add_argument("--precinct-election-and-demographics", help = 'input for block level demographic data as geojson', required=True)
parser.add_argument("-d", help = "output directory", required=True)
args = parser.parse_args()

# Make the output directory if it does not exist
if not os.path.exists(args.d):
    os.makedirs(args.d)

precinct_election_and_demographics = gpd.read_file(args.precinct_election_and_demographics)

# Calculate adjacency graph using rook adjacency
dual_graph = Graph.from_geodataframe(precinct_election_and_demographics)

# Export graph to be used by MGGG algorithm
dual_graph.to_json(args.d + "\\adjacency_graph.json")