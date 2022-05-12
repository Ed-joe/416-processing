import math

from gerrychain import (GeographicPartition, Graph, MarkovChain, updaters, constraints, accept, Election, metrics)
import pandas


# TODO Make a dictionary entry for each demographic
def num_majority_minority(partition, group_ids):
    num_districts = 0
    for district in partition.parts:
        majority = "white_pop"
        for group in group_ids:
            if partition[group][district] > partition[majority][district]:
                majority = group
        if not "white_pop":
            num_districts += 1

    return num_districts


def polsby_popper_values(partition):
    return metrics.polsby_popper(partition)


def efficiency_gap(partition):
    return metrics.efficiency_gap(partition)


election = Election("2020_presidential", {"Democratic": "DEMOCRAT", "Republican": "REPUBLICAN"})
partition_updaters = {
    "2020_presidential": election,
    "total_pop": updaters.Tally("TOTAL_POPULATION"),
    "hispanic_pop": updaters.Tally("HISPANIC_LATINO"),
    "white_pop": updaters.Tally("WHITE"),
    "black_pop": updaters.Tally("AFRICAN_AMERICAN"),
    "amer_indian_pop": updaters.Tally("AMERICAN_INDIAN"),
    "asian_pop": updaters.Tally("ASIAN"),
    "pacific_pop": updaters.Tally("PACIFIC_ISLANDER")
}
test = {
    "hispanic_pop": updaters.Tally("HISPANIC_LATINO"),
    "white_pop": updaters.Tally("WHITE"),
    "black_pop": updaters.Tally("AFRICAN_AMERICAN"),
    "amer_indian_pop": updaters.Tally("AMERICAN_INDIAN"),
    "asian_pop": updaters.Tally("ASIAN"),
    "pacific_pop": updaters.Tally("PACIFIC_ISLANDER")
}
precincts_graph = Graph.from_json("C:\\Users\\Admin\\PycharmProjects\\CSE416PREPRO\\output\\nv\\adjacency_graph.json")
mapping = pandas.read_csv("C:\\Users\\Admin\\PycharmProjects\\CSE416PREPRO\\output\\nv\\mapping.csv")

test_partition = GeographicPartition(precincts_graph, assignment=mapping["0"].to_dict(),
                                     updaters=partition_updaters)
# num_majority_minority(test_partition, test)
print(polsby_popper_values(test_partition))
print(efficency_gap(test_partition["2020_presidential"]))
