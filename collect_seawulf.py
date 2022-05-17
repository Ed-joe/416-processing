from os import listdir
from os.path import isfile, join
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Collect all of the seawulf data and make a new file combining them')
parser.add_argument("--path", help='path to the output directory that you are aggregating',
                    required=True)
parser.add_argument("-n", help='the state code', required=True)
parser.add_argument("-d", help="output directory", required=True)
args = parser.parse_args()

plans = [join(args.path, f) for f in listdir(args.path) if isfile(join(args.path, f)) and f.endswith(".json")]

districting_metrics = pd.DataFrame(columns=["num_majority_minority", "combined_num_majority_minority",
                                            "rep_dem_splits", "polsby_popper_mean", "efficiency_gap",
                                            "seat_vote_points", "box_and_whisker_data"])
for plan in plans:
    df_row = pd.read_json(plan, orient="index")
    districting_metrics = pd.concat([districting_metrics, df_row], ignore_index=True)
    print(plan + " has been added")
districting_metrics.to_json(args.d + "/combined_districts_" + args.n + ".json", orient="index")
