def calculate_box_and_whisker(partition, group_ids, total_pop_id):
    # initialize dictionary to map basis to population percentage in each district
    group_percentages_dict = {}
    for g in group_ids:
        group_percentages_dict[g] = []

    # get percentages using partition object which keeps track of population by grouping and total pop
    for g in group_ids:
        for district_id in range(len(partition)):
            group_percentages_dict[g].append(partition[g][district_id] / partition[total_pop_id][district_id])
    
    # sort percentages in ascending order
    for g in group_ids:
        group_percentages_dict[g].sort()
    
    return group_percentages_dict
