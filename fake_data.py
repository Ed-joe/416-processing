import random
import mysql.connector

mydb = mysql.connector.connect(
    host='mysql3.cs.stonybrook.edu',
    user='rjwillett',
    password='112001203',
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

mydb.commit()