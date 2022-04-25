import numpy
from gerrychain import Partition, Graph

def calculate_box_and_whisker(partition, groups):
    # initialize dictionary to map basis to population percentage in each district
    group_percentages_dict = {}
    for g in groups:
        group_percentages_dict[g] = []

    # for each district in the partition
    for district in partition.parts:
        # initialize populations for this district
        total_pop = 0
        for g in groups:
            group_percentages_dict[g].append(0)
        
        # for each precinct in the district
        for precinct in TODO:
            for g in groups:
                group_percentages_dict[g][-1] += TODO PRECINCT POPULATION OF GROUP

