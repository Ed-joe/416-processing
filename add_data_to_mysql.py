import mysql.connector
import os

import geopandas as gpd
import pandas as pd
import math


### POLSBY POPPER HELPER FUNC
def calculate_compactness(geom):
    p = geom.length
    a = geom.area
    return (4 * math.pi * a) / (p * p)



mydb = mysql.connector.connect(
    host='mysql3.cs.stonybrook.edu',
    user='',
    password='',
    database='Sparks'
)

mycursor = mydb.cursor()


# constants
political_group_keys = ['AFRICAN_AMERICAN','AMERICAN_INDIAN','ASIAN','DEMOCRAT','HISPANIC_LATINO','PACIFIC_ISLANDER','REPUBLICAN','TOTAL_POPULATION','WHITE']

# counters to keep track of ids
precinct_id = 0
district_id = 0
district_plan_id = 0
state_id = 0

# iterate over each state
states_list = ["nv", "il", "pa"]
for folder in states_list:
    ### STATE LEVEL DATA
    sql = 'INSERT INTO state (state_id, state_code, seawulf_seat_share_bias_at50, seawulf_seat_share_responsiveness, seawulf_seat_share_symmetry) VALUES (%s, %s, %s, %s, %s)'
    val = (
        state_id,
        folder,
        0,
        0,
        0
    )
    # @TODO
    mycursor.execute(sql, val)
    print('inserted', folder, 'state data')


    ### PRECINCT LEVEL DATA
    curr_precincts = gpd.read_file('../output/' + folder + '/precinct_level_elections_and_demographics.json')
    curr_precinct_id_list = []

    # iterate over precinct by index
    for i in range(len(curr_precincts)):
        # store this precinct in mysql
        sql = 'INSERT INTO precinct (precinct_id, name) VALUES (%s, %s)'
        val = (
            precinct_id,
            curr_precincts['precinct_name'][i]
        )
        # @TODO
        mycursor.execute(sql, val)

        # store precinct demographic and election data
        for group in political_group_keys:
            sql = 'INSERT INTO precinct_demographic_and_election_data (precinct_id, demographic_and_election_data, demographic_and_election_data_key) VALUES (%s, %s, %s)'
            val = (
                precinct_id,
                curr_precincts[group][i].item(),
                political_group_keys.index(group)
            )
            # @TODO
            mycursor.execute(sql, val)

        # store this precinct's id in column list
        curr_precinct_id_list.append(precinct_id)
        # update id counter
        precinct_id += 1
    print('inserted', folder, 'precinct data')

    ### DISTRICT/DISTRICT PLAN LEVEL DATA
    districting_dir = '../raw_data/' + folder + '_plans/'
    districtings = os.listdir(districting_dir)
    districtings.remove('.DS_Store')

    district_id_list = {}
    
    # for each district plan
    for districting_file in districtings:
        curr_districting = gpd.read_file(districting_dir + districting_file)
        id_list_key = districting_file[17:len(districting_file)-5]
        district_id_list[id_list_key] = []

        # calculate average polsby popper
        compactness_list = curr_districting.geometry.apply(calculate_compactness)
        avg_compactness = sum(compactness_list) / len(compactness_list)

        sql = 'INSERT INTO district_plan (district_plan_id, compactness, name, state_id) VALUES (%s, %s, %s, %s)'
        val = (
            district_plan_id,
            avg_compactness,
            id_list_key,
            state_id
        )
        # @TODO
        mycursor.execute(sql, val)

        # for each district in this plan
        for i in range(len(curr_districting)):
            sql = 'INSERT INTO district (district_id, district_plan_id) VALUES (%s, %s)'
            val = (
                district_id,
                district_plan_id
            )
            # @TODO
            mycursor.execute(sql, val)
            district_id_list[id_list_key].append(district_id)
            district_id += 1

        district_plan_id += 1
    print('inserted', folder, 'district plan/district data')

    ### PRECINCT DISTRICT MAPPING DATA
    # get mapping csv names from folders
    mappings_dir = '../output/' + folder + '/mappings/'
    mappings = os.listdir(mappings_dir)
    mappings.remove('.DS_Store')
    
    # for each district plan
    sql = 'INSERT INTO precinct_district_map (district_id, precinct_id) VALUES (%s, %s)'
    for map_file in mappings:
        id_list_key = map_file[0:len(map_file)-12]
        with open(mappings_dir + map_file, 'r') as file_reader:
            next(file_reader)
            for line in file_reader:
                line = line.strip()
                p_id, d_id = line.split(',')
                val = (
                    district_id_list[id_list_key][int(d_id)],
                    curr_precinct_id_list[int(p_id)]
                )
                # @TODO
                mycursor.execute(sql, val)
        print('inserted', id_list_key, 'mapping data')

    print('finished saving', folder)
    state_id += 1

mydb.commit()