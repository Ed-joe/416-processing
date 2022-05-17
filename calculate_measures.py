# import math
import statistics
from gerrychain import (GeographicPartition, Graph, updaters, Election, metrics)
# import pandas
from generate_seat_vote_curve import generate_seat_vote_curve
# import matplotlib.pyplot as plt
# import box_and_whisker as bx


def num_combined_majority_minority(partition, group_ids):
    districts_comb_majority_minority = 0
    for district in partition.parts:
        minority_sum = 0
        for group in group_ids:
            if group != "white_pop":
                minority_sum += partition[group][district]
        if minority_sum / partition["total_pop"][district] > partition["white_pop"][district] / partition["total_pop"][
                                                                                                              district]:
            districts_comb_majority_minority += 1
    return districts_comb_majority_minority


def num_majority_minority_map(partition, group_ids):
    demographics = dict.fromkeys(group_ids, 0)
    for district in partition.parts:
        majority = "white_pop"
        for group in group_ids:
            if partition[group][district] > partition[majority][district]:
                majority = group
        if majority != "white_pop":
            demographics[majority] += 1

    return demographics


def calculate_rep_dem_splits(election_object):
    party_to_wins_map = {}
    for party in election_object.election.parties:
        party_to_wins_map[party] = election_object.wins(party)
    return party_to_wins_map


def polsby_popper_mean(partition):
    return statistics.mean(metrics.polsby_popper(partition).values())


def efficiency_gap(election_object):
    return metrics.efficiency_gap(election_object)


def generate_sv_curve(election_object):
    rep_counts = election_object.counts("Republican")
    dem_counts = election_object.counts("Democratic")
    seat_vote_formatted_input = []
    for i in range(len(rep_counts)):
        seat_vote_formatted_input.append(str(rep_counts[i]) + "," + str(dem_counts[i]))

    return generate_seat_vote_curve(seat_vote_formatted_input)

#
# election = Election("2020_presidential", {"Democratic": "DEMOCRAT", "Republican": "REPUBLICAN"})
# partition_updaters = {
#     "2020_presidential": election,
#     "total_pop": updaters.Tally("TOTAL_POPULATION"),
#     "hispanic_pop": updaters.Tally("HISPANIC_LATINO"),
#     "white_pop": updaters.Tally("WHITE"),
#     "black_pop": updaters.Tally("AFRICAN_AMERICAN"),
#     "amer_indian_pop": updaters.Tally("AMERICAN_INDIAN"),
#     "asian_pop": updaters.Tally("ASIAN"),
#     "pacific_pop": updaters.Tally("PACIFIC_ISLANDER")
# }
# test = {
#     "hispanic_pop": updaters.Tally("HISPANIC_LATINO"),
#     "black_pop": updaters.Tally("AFRICAN_AMERICAN"),
#     "amer_indian_pop": updaters.Tally("AMERICAN_INDIAN"),
#     "asian_pop": updaters.Tally("ASIAN"),
#     "pacific_pop": updaters.Tally("PACIFIC_ISLANDER")
# }
# precincts_graph = Graph.from_json("C:\\Users\\Owner\\PycharmProjects\\416-preprocessing\\output\\nv"
#                                   "\\adjacency_graph.json")
# mapping = pandas.read_csv("C:\\Users\\Owner\\PycharmProjects\\416-preprocessing\\output\\nv\\mapping.csv")
#
# test_partition = GeographicPartition(precincts_graph, assignment=mapping["0"].to_dict(),
#                                      updaters=partition_updaters)
# num_majority_minority_map(test_partition, test)
# print(polsby_popper_mean(test_partition))
# print(efficiency_gap(test_partition["2020_presidential"]))
# print(calculate_rep_dem_splits(test_partition["2020_presidential"]))
# print(num_combined_majority_minority(test_partition, test))
# sv_lists = generate_sv_curve(test_partition["2020_presidential"])

# x, y = zip(*sv_lists[0])
# x2, y2 = zip(*sv_lists[1])
# plt.plot(x, y)
# plt.plot(x2, y2)
# plt.show()
# print(bx.calculate_box_and_whisker(test_partition, test.keys(), "total_pop"))
