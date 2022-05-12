import sys
import random


# source: https://github.com/jeffreyshen19/Seats-Votes-Curves/blob/master/generator/uniform_partisan_swing.py

# data should be in form ["rep_votes,dem_votes","rep_votes,dem_votes",...] where each index element represents
# a district and the party votes are the totals for that district
# ouput file does not have to exist but the folder(s) it its stored in must exist
def generate_seat_vote_curve(data):
    # initialize district level results list
    voting_by_district = []

    # initialize results storage lists
    seats_votes_rep = []
    seats_votes_dem = []

    # Percentage to increase each district by
    SWING_CONST = 0.005

    # initialize more 
    total_votes = 0
    total_dem_votes = 0
    total_rep_votes = 0

    # Read and store all district data
    for line_str in data:
        if len(line_str) > 0:
            line = line_str.split(",")
            rep = int(line[0])
            dem = int(line[1])
            total = rep + dem

            total_votes += total
            total_dem_votes += dem
            total_rep_votes += rep
            percent_rep = float(rep) / total

            voting_by_district.append({"percent_rep": percent_rep, "percent_dem": 1.0 - percent_rep})

    # calculate starting points for rep and dem main loops
    rep_vote_share = float(total_rep_votes) / total_votes
    dem_vote_share = float(total_dem_votes) / total_votes

    diff = (((100 * rep_vote_share) % 1) - ((100 * dem_vote_share) % 1)) / 100

    # main rep loop
    i = rep_vote_share
    counter = 0
    while i <= 1:
        # initialize counters
        total_rep_seats = 0
        total_dem_seats = 0

        for _ in range(1000):  # simulate 1000 elections
            # tell us which districts overflowed, if any
            district_overflowed_rep = [False] * len(voting_by_district)
            district_overflowed_dem = [False] * len(voting_by_district)

            # count excess votes
            excess_dem = 0
            excess_rep = 0

            # give us district vote counts
            updated_vals_rep = [0] * len(voting_by_district)
            updated_vals_dem = [0] * len(voting_by_district)

            for k, district in enumerate(voting_by_district):  # iterate over each district
                # get percentage of this district's rep/dem votes
                updated_vals_rep[k] = district["percent_rep"] + counter * SWING_CONST + SWING_CONST * random.randint(-5,
                                                                                                                     5)
                updated_vals_dem[k] = 1 - updated_vals_rep[k] + diff

                # account for overflow votes
                if updated_vals_rep[k] > 1:
                    excess_rep += 1
                    district_overflowed_rep[k] = True
                if updated_vals_dem[k] < 0:
                    excess_dem += 1
                    district_overflowed_dem[k] = True

            for k, district in enumerate(voting_by_district):  # iterate over each district
                # Overflow mechanic: distribute excess votes to the other districts
                if not district_overflowed_rep[k]:
                    updated_vals_rep[k] += SWING_CONST * (excess_rep / (len(voting_by_district) - excess_rep))
                if not district_overflowed_dem[k]:
                    updated_vals_dem[k] -= SWING_CONST * (excess_dem / (len(voting_by_district) - excess_dem))

                if updated_vals_rep[k] > 0.50:
                    total_rep_seats += 1
                if updated_vals_dem[k] > 0.50:
                    total_dem_seats += 1

        # update loop counters
        i += SWING_CONST
        counter += 1

        # store generated seat curve data
        if i <= 1:
            seats_votes_rep.append((i, float(total_rep_seats) / (len(voting_by_district) * 1000.0)))
            seats_votes_dem.insert(0, (1 - i + diff, float(total_dem_seats) / (len(voting_by_district) * 1000.0)))

    # main dem loop
    i = dem_vote_share
    counter = 0
    while i <= 1:
        total_dem_seats = 0
        total_rep_seats = 0

        for j in range(0, 1000):  # simulate 1000 elections
            district_overflowed_rep = [False] * len(voting_by_district)
            district_overflowed_dem = [False] * len(voting_by_district)
            excess_dem = 0
            excess_rep = 0
            updated_vals_rep = [0] * len(voting_by_district)
            updated_vals_dem = [0] * len(voting_by_district)

            for k, district in enumerate(voting_by_district):
                updated_vals_dem[k] = district["percent_dem"] + counter * SWING_CONST + SWING_CONST * random.randint(-5,
                                                                                                                     5) + diff
                updated_vals_rep[k] = 1 - (updated_vals_dem[k] - diff)

                if updated_vals_rep[k] > 1:
                    excess_rep += 1
                    district_overflowed_rep[k] = True

                if updated_vals_dem[k] < 0:
                    excess_dem += 1
                    district_overflowed_dem[k] = True

            for k, district in enumerate(voting_by_district):
                # Overflow mechanic: distribute excess votes to the other districts
                if district_overflowed_rep[k] is False:
                    updated_vals_rep[k] -= SWING_CONST * (excess_rep / (len(voting_by_district) - excess_rep))

                if district_overflowed_dem[k] is False:
                    updated_vals_dem[k] += SWING_CONST * (excess_dem / (len(voting_by_district) - excess_dem))

                if updated_vals_rep[k] > 0.50:
                    total_rep_seats += 1
                if updated_vals_dem[k] > 0.50:
                    total_dem_seats += 1

        i += SWING_CONST
        counter += 1

        if i <= 1:
            seats_votes_dem.append(
                (i + diff, float(total_dem_seats) / (len(voting_by_district) * 1000.0)))
            seats_votes_rep.insert(0, (1 - i, float(total_rep_seats) / (len(voting_by_district) * 1000.0)))

    # Add endpoints
    seats_votes_rep.insert(0, (0, 0))
    seats_votes_dem.insert(0, (0, 0))
    seats_votes_rep.append((1, 1))
    seats_votes_dem.append((1, 1))


    return seats_votes_rep, seats_votes_dem
