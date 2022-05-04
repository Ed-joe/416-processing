import random
from tkinter import Y
import mysql.connector
import math

mydb = mysql.connector.connect(
    host='mysql3.cs.stonybrook.edu',
    user='aajith',
    password='112164070',
    database='Sparks'
)

mycursor = mydb.cursor()

def rand_to_sum(num_vals, max):
    values = []
    for i in range(num_vals - 1):
        values.append(random.randint(0, max))
    values.sort()
    final = []
    current = 0
    for val in values:
        final.append(val - current)
        current = val
    final.append(max - current)
    return final


#FAKE NEVADA
# sql = 'INSERT INTO state (state_id, state_code) VALUES (%s, %s)'
# val = (12, 'NY')
# mycursor.execute(sql, val)

# Dummy seawulf box and whisker data
# sql = 'INSERT INTO seawulf_box_and_whisker_data (state_id, political_group, lower_quartile, maximum, median, minimum, upper_quartile) VALUES (%s, %s, %s, %s, %s, %s, %s)'

# for i in range(4):
#     for i in range(7):
#         values = random.sample(range(1, 20), 5)
#         values.sort()
#         mycursor.execute(sql, (5, i, values[1], values[4], values[2], values[0], values[3]))

# # Dummy seawulf majority minority data
# counts = rand_to_sum(35, 10000)

# sql = 'INSERT INTO seawulf_majority_minority (state_id, count, num_majority_minority_districts, political_group) VALUES (%s, %s, %s, %s)'

# iter = 0
# for i in range(7):
#     for j in range(5):
#         values = [5]
#         values.append(counts[iter])
#         values.append(j)
#         values.append(i)
#         mycursor.execute(sql, values)
#         iter += 1

# # DUMMY SEAWULF DEMOCRAT SEAT VOTE DATA
# sql = 'INSERT INTO seawulf_democrat_seat_share (state_id, x, y) VALUES (%s, %s, %s)'
# mycursor.execute(sql, (5, 0, 0))
# for i in range(1, 100):
#     y = (100 / (1 + math.exp(7.8 + 1.2*(-.12 * i))))
#     mycursor.execute(sql, (5, i, y))
# mycursor.execute(sql, (5, 100, 100))
    
# # DUMMY SEAWULF REPUBLICAN SEAT VOTE DATA
# sql = 'INSERT INTO seawulf_republican_seat_share (state_id, x, y) VALUES (%s, %s, %s)'
# mycursor.execute(sql, (5, 0, 0))
# for i in range(100):
#     y = (100 / (1 + math.exp(6.5 + 1.2*(-.1 * i))))
#     mycursor.execute(sql, (5, i, y))
# mycursor.execute(sql, (5, 100, 100))

# # DUMMY SEAWULF REP DEM SPLIT DATA
# sql = 'INSERT INTO seawulf_republican_democrat_split (state_id, count, democrat_seats, republican_seats) VALUES (%s, %s, %s, %s)'
# counts = rand_to_sum(5, 10000)
# for i in range(5):
#     mycursor.execute(sql, (5, counts[i], i, 4 - i))


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