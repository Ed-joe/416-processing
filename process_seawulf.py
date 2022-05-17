import argparse
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)

parser = argparse.ArgumentParser(description='Process Seawulf and prepare for db insertion')
parser.add_argument("--path", help='file path to process',
                    required=True)
parser.add_argument("--num", help='number of districts', required=True)
parser.add_argument("-n", help='the state code', required=True)
parser.add_argument("-d", help="output directory", required=True)
args = parser.parse_args()

seawulf_data = pd.read_json(args.path, orient="index")

demographic_map = {"black_pop": 0, "amer_indian_pop": 1, "asian_pop": 2, "hispanic_pop": 4,
                   "pacific_pop": 5, "white_pop": 8}

num_districts = int(args.num)

# Prepare num_majority_minority histogram data
num_majority_minority_column = seawulf_data["num_majority_minority"]
nmm_histogram_data = pd.DataFrame(columns=["basis", "num_majority_minority", "count"])
for group in demographic_map.keys():
    for num_majority_minority_x in range(0, num_districts + 1):
        tally_for_count = 0
        for index, row in num_majority_minority_column.iteritems():
            if row[group] == num_majority_minority_x:
                tally_for_count += 1
        nmm_histogram_data = nmm_histogram_data.append(
            {"basis": demographic_map[group], "num_majority_minority": num_majority_minority_x,
             "count": tally_for_count}, ignore_index=True)

nmm_histogram_data.to_csv(args.d + "/num_majority_minority_" + args.n + ".csv")

# Prepare combined majority minority histogram data
combined_majority_minority_column = seawulf_data["combined_num_majority_minority"]
ncmm_histogram_data = pd.DataFrame(columns=["num_combined_majority_minority_districts", "count"])

for num_combined_majority_minority_x in range(0, num_districts + 1):
    tally_for_count = 0
    for index, row in combined_majority_minority_column.iteritems():
        if row == num_combined_majority_minority_x:
            tally_for_count += 1
    ncmm_histogram_data = ncmm_histogram_data.append(
        {"num_combined_majority_minority_districts": num_combined_majority_minority_x,
         "count": tally_for_count}, ignore_index=True)

ncmm_histogram_data.to_csv(args.d + "/num_combined_majority_minority_" + args.n + ".csv")
# Prepare Republican Democrat Splits Data
different_splits = []
democrat_split = num_districts
republican_split = 0
rd_splits_column = seawulf_data["rep_dem_splits"]
splits_histogram_data = pd.DataFrame(columns=["count", "democrat_seats", "republican_seats"])
for i in range(0, num_districts + 1):
    different_splits.append((democrat_split, republican_split))
    democrat_split -= 1
    republican_split += 1

for split in different_splits:
    tally_for_count = 0
    for index, row in rd_splits_column.iteritems():
        if (row["Democratic"], row["Republican"]) == split:
            tally_for_count += 1
    splits_histogram_data = splits_histogram_data.append(
        {"count": tally_for_count, "democrat_seats": split[0], "republican_seats": split[1]}, ignore_index=True)

splits_histogram_data.to_csv(args.d + "/rep_dem_splits_" + args.n + ".csv")

# Prepare polsby popper histogram
compactness_column = seawulf_data["polsby_popper_mean"]
compactness_histogram_data = pd.DataFrame(columns=["count", "min_range", "max_range"])
compactness_ranges = {}
for i in np.arange(0, 1, .04):
    compactness_ranges[(np.round(i, 2), np.round(i + .04, 2))] = 0

for index, row in compactness_column.iteritems():
    for compactness_range in compactness_ranges.keys():
        if compactness_range[0] <= row < compactness_range[1]:
            compactness_ranges[compactness_range] += 1
            break
for compactness_range, tally_for_count in compactness_ranges.items():
    if tally_for_count != 0:
        compactness_histogram_data = compactness_histogram_data.append(
            {"count": tally_for_count, "min_range": compactness_range[0], "max_range": compactness_range[1]},
            ignore_index=True)

compactness_histogram_data.to_csv(args.d + "/compactness_" + args.n + ".csv")

# Prepare efficiency_gap histogram
efficiency_gap_column = seawulf_data["efficiency_gap"]
efficiency_gap_histogram_data = pd.DataFrame(columns=["count", "min_range", "max_range"])
efficiency_gap_ranges = {}
for i in np.arange(-.5, 5, .05):
    efficiency_gap_ranges[(np.round(i, 2), np.round(i + .05, 2))] = 0

for index, row in efficiency_gap_column.iteritems():
    for efficiency_gap_range in efficiency_gap_ranges.keys():
        if efficiency_gap_range[0] <= row < efficiency_gap_range[1]:
            efficiency_gap_ranges[efficiency_gap_range] += 1
            break
for efficiency_gap_range, tally_for_count in efficiency_gap_ranges.items():
    if tally_for_count != 0:
        efficiency_gap_histogram_data = efficiency_gap_histogram_data.append(
            {"count": tally_for_count, "min_range": efficiency_gap_range[0], "max_range": efficiency_gap_range[1]},
            ignore_index=True)

efficiency_gap_histogram_data.to_csv(args.d + "/efficiency_gap_" + args.n + ".csv")

# Prepare seat_votes curve data
seat_votes_column = seawulf_data["seat_vote_points"]
seat_votes_republican_data = pd.DataFrame(columns=["x", "y"])
seat_votes_democrat_data = pd.DataFrame(columns=["x", "y"])
republican_plots = [info[0] for index, info in seat_votes_column.iteritems()]
democratic_plots = [info[1] for index, info in seat_votes_column.iteritems()]

republican_average_plot = np.average(republican_plots, axis=0)
democratic_average_plot = np.average(democratic_plots, axis=0)

for point in republican_average_plot:
    seat_votes_republican_data = seat_votes_republican_data.append({"x": point[0], "y": point[1]}, ignore_index=True)

for point in democratic_average_plot:
    seat_votes_democrat_data = seat_votes_democrat_data.append({"x": point[0], "y": point[1]}, ignore_index=True)

seat_votes_democrat_data.to_csv(args.d + "/democrat_seat_vote_" + args.n + ".csv")
seat_votes_republican_data.to_csv(args.d + "/republican_seat_vote_" + args.n + ".csv")

# calculate bias at 50
rep_closest_to_50 = min(republican_average_plot, key=lambda x: abs(x[0] - .5))
dem_closest_to_50 = min(democratic_average_plot, key=lambda x: abs(x[0] - .5))
bias_at_50 = rep_closest_to_50[1] - dem_closest_to_50[1]

# symmetry
rep_points = list(filter(lambda x: abs(x[0]-.5) < .05, republican_average_plot))
dem_points = list(filter(lambda x: abs(x[0]-.5) < .05, democratic_average_plot))
symmetry = 0
for i in range(len(rep_points)):
    symmetry += abs(rep_points[i][1] - dem_points[i][1])

symmetry /= len(rep_points)

# responsiveness
average_dem_slope = (dem_points[-1][1] - dem_points[0][1])/(dem_points[-1][0] - dem_points[0][0])
average_rep_slope = (rep_points[-1][1] - rep_points[0][1])/(rep_points[-1][0] - rep_points[0][0])
responsiveness = (average_rep_slope + average_dem_slope)/2

seat_votes_metrics = pd.DataFrame(columns=["bias_at_50", "symmetry", "responsiveness"])
seat_votes_metrics = seat_votes_metrics.append({"bias_at_50": bias_at_50, "symmetry": symmetry, "responsiveness": responsiveness}, ignore_index=True)
seat_votes_metrics.to_csv(args.d + "/seat_vote_avg_metrics_" + args.n + ".csv")

# Prepare Box and Whisker
box_and_whisker_column = seawulf_data["box_and_whisker_data"]
box_and_whisker_data = pd.DataFrame(
    columns=["lower_quartile", "maximum", "median", "minimum", "political_group", "upper_quartile", "mean"])
for group in demographic_map:
    group_lists = [group_list[group] for index, group_list in box_and_whisker_column.iteritems()]
    for i in range(0, num_districts):
        indexed_elements = sorted([item[i] for item in group_lists])
        median = np.median(indexed_elements)
        mean = np.mean(indexed_elements)
        maximum = indexed_elements[-1]
        minimum = indexed_elements[0]
        lower_quartile = np.quantile(indexed_elements, .25)
        upper_quartile = np.quantile(indexed_elements, .75)
        box_and_whisker_data = box_and_whisker_data.append(
            {"lower_quartile": lower_quartile, "maximum": maximum, "median": median, "minimum": minimum,
             "political_group": demographic_map[group], "upper_quartile": upper_quartile, "mean": mean},
            ignore_index=True)

box_and_whisker_data.to_csv(args.d + "/box_and_whisker_" + args.n + ".csv")
