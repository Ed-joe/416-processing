import random
import mysql.connector
import geopandas as gpd
import pandas as pd

mydb = mysql.connector.connect(
    host='mysql3.cs.stonybrook.edu',
    user='ejcarey',
    password='112029315',
    database='Sparks'
)

mycursor = mydb.cursor()

# FAKE NEVADA
# sql = 'INSERT INTO state (state_id, state_code) VALUES (%s, %s)'
# val = (5, 'NV')
# mycursor.execute(sql, val)


# DELETE AND CREATE 4 RANDOM DISTRICT PLANS
# sql = 'DELETE FROM district_plan'
# mycursor.execute(sql, ())
# count = 0
# for name in ['Approved Plan', 'Proposed Democrat Plan', 'Proposed Republican Plan', 'Old Republican Plan']:
#     sql = 'INSERT INTO district_plan (district_plan_id, compactness, efficiency_gap, fairness, mean_population_deviation, name, num_competitive_districts, num_minority_majority_districts, seat_share_bias_at50, seat_share_responsiveness, seat_share_symmetry, state_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#     val = (
#         count,
#         random.random() / 2 + .5,
#         random.random() / 2,
#         random.random(),
#         random.random() / 10,
#         name,
#         random.choice([0, 0, 0, 0, 1]),
#         random.choice([0, 0, 0, 1, 2]),
#         random.random() * 100,
#         random.random() * 10 + 5,
#         random.random(),
#         5
#     )
#     count += 1
#     mycursor.execute(sql, val)
#
# count = 0
# for i in range(0, 4):
#     sql = 'INSERT INTO district (district_id, district_plan_id) VALUES (%s, %s)'
#     val = (
#         count,
#         0
#     )
#     count += 1
#     mycursor.execute(sql, val)

# count = 0

# for index, row in data.iterrows():
#     sql = 'INSERT INTO precinct (precinct_id, name) VALUES (%s, %s)'
#     val = (
#         index,
#         row["precinct_name"]
#     )
#     count += 1
#     mycursor.execute(sql, val)

# data = gpd.read_file("C:\\Users\\Admin\\PycharmProjects\\CSE416PREPRO\\output\\test.geojson")
# data = data.fillna(0)
# demographic_map = {"black_pop": 0, "amer_indian_pop": 1, "asian_pop": 2, "2020_biden_votes": 3, "hispanic_pop": 4,
#                    "pacific_pop": 5, "2020_trump_votes": 6,
#                    "total_pop": 7, "white_pop": 8}
# for index, row in data.iterrows():
#     for demographic in demographic_map.keys():
#         sql = 'INSERT INTO precinct_demographic_and_election_data (precinct_id, demographic_and_election_data, demographic_and_election_data_key) VALUES (%s, %s, %s)'
#         val = (
#             index,
#             row[demographic],
#             demographic_map[demographic]
#         )
#         mycursor.execute(sql, val)

nv_proposed_plan_mapping = pd.read_csv("C:\\Users\\Admin\\PycharmProjects\\CSE416PREPRO\\output\\nv_mapping.csv", index_col=[0])
for index, row in nv_proposed_plan_mapping.iterrows():
    sql = 'INSERT INTO precinct_district_map (district_id, precinct_id) VALUES (%s, %s)'
    val = (
        row[0].item(),
        index
    )
    mycursor.execute(sql, val)

mydb.commit()
