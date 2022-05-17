import mysql.connector
import os

import geopandas as gpd
import pandas as pd
import math

mydb = mysql.connector.connect(
    host='mysql3.cs.stonybrook.edu',
    user='ejcarey',
    password='112029315',
    database='Sparks'
)

mycursor = mydb.cursor()

state_code = "pa"
state_id = 2

input_directory = "./output/pa_sw_for_db/"

# Box and whisker
box_and_whisker_data = pd.read_csv(input_directory + "box_and_whisker_" + state_code + ".csv")
for index, row in box_and_whisker_data.iterrows():
    sql = 'INSERT INTO seawulf_box_and_whisker_data (state_id, lower_quartile, maximum, median, minimum, political_group, upper_quartile, mean) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    val = (
        state_id,
        row["lower_quartile"],
        row["maximum"],
        row["median"],
        row["minimum"],
        row["political_group"],
        row["upper_quartile"],
        row["mean"]
    )
    # @TODO
    mycursor.execute(sql, val)

# compactness
compactness_data = pd.read_csv(input_directory + "compactness_" + state_code + ".csv")
for index, row in compactness_data.iterrows():
    sql = 'INSERT INTO seawulf_compactness (state_id, count, range_maximum, range_minimum) VALUES (%s, %s, %s, %s)'
    val = (
        state_id,
        row["count"],
        row["max_range"],
        row["min_range"]
    )
    # @TODO
    mycursor.execute(sql, val)

# democrat_seat_vote
democrat_seat_vote_data = pd.read_csv(input_directory + "democrat_seat_vote_" + state_code + ".csv")
for index, row in democrat_seat_vote_data.iterrows():
    sql = 'INSERT INTO seawulf_democrat_seat_share (state_id, x, y) VALUES (%s, %s, %s)'
    val = (
        state_id,
        row["x"],
        row["y"]
    )

    # @TODO
    mycursor.execute(sql, val)

# republican_seat_vote
republican_seat_vote_data = pd.read_csv(input_directory + "republican_seat_vote_" + state_code + ".csv")
for index, row in republican_seat_vote_data.iterrows():
    sql = 'INSERT INTO seawulf_republican_seat_share (state_id, x, y) VALUES (%s, %s, %s)'
    val = (
        state_id,
        row["x"],
        row["y"]
    )
    # @TODO
    mycursor.execute(sql, val)

# seat_vote_metrics
seat_vote_metrics = pd.read_csv(input_directory + "seat_vote_avg_metrics_" + state_code + ".csv")
sql_sv = "UPDATE state SET seawulf_seat_share_bias_at50 = %s WHERE state_id = %s"
val = (
    float(seat_vote_metrics["bias_at_50"]),
    state_id
)
mycursor.execute(sql_sv, val)

sql_sv = "UPDATE state SET seawulf_seat_share_symmetry = %s WHERE state_id = %s"
val = (
    float(seat_vote_metrics["symmetry"]),
    state_id
)
mycursor.execute(sql_sv, val)

sql_sv = "UPDATE state SET seawulf_seat_share_responsiveness = %s WHERE state_id = %s"
val = (
    float(seat_vote_metrics["responsiveness"]),
    state_id
)
mycursor.execute(sql_sv, val)


# efficiency_gap
efficiency_gap_data = pd.read_csv(input_directory + "efficiency_gap_" + state_code + ".csv")
for index, row in efficiency_gap_data.iterrows():
    sql = 'INSERT INTO seawulf_efficiency_gap (state_id, count, range_maximum, range_minimum) VALUES (%s, %s, %s, %s)'
    val = (
        state_id,
        row["count"],
        row["max_range"],
        row["min_range"]
    )

    # @TODO
    mycursor.execute(sql, val)

# num combined majority minority
num_combined_majority_minority_data = pd.read_csv(input_directory + "num_combined_majority_minority_" + state_code + ".csv")
for index, row in num_combined_majority_minority_data.iterrows():
    sql = 'INSERT INTO seawulf_combined_majority_minority (state_id, count, num_combined_majority_minority_districts) VALUES (%s, %s, %s)'
    val = (
        state_id,
        int(row["count"]),
        int(row["num_combined_majority_minority_districts"])
    )
    # @TODO
    mycursor.execute(sql, val)

# majority minority
num_majority_minority_data = pd.read_csv(input_directory + "num_majority_minority_" + state_code + ".csv")
for index, row in num_majority_minority_data.iterrows():
    sql = 'INSERT INTO seawulf_majority_minority (state_id, count, num_majority_minority_districts, political_group) VALUES (%s, %s, %s, %s)'
    val = (
        state_id,
        int(row["count"]),
        int(row["num_majority_minority"]),
        int(row["basis"])
    )
    # @TODO
    mycursor.execute(sql, val)

# rep_dem_splits
rep_dem_splits = pd.read_csv(input_directory + "rep_dem_splits_" + state_code + ".csv")
for index, row in rep_dem_splits.iterrows():
    sql = 'INSERT INTO seawulf_republican_democrat_split (state_id, count, democrat_seats, republican_seats) VALUES (%s, %s, %s, %s)'
    val = (
        state_id,
        int(row["count"]),
        int(row["democrat_seats"]),
        int(row["republican_seats"])
    )
    # @TODO
    mycursor.execute(sql, val)



mydb.commit()
