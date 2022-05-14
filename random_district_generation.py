import argparse
import json
from functools import partial
from gerrychain import (GeographicPartition, Graph, MarkovChain, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
import pandas as pd
import calculate_measures as sw_measures
import box_and_whisker
import warnings

class RandomDistrictGenerator:
    def __init__(self, precincts_graph_path, state_id, num_chain_iterations, num_random_districtings,
                 precinct_mapping_path, output_data_path, population_deviation_threshold, target_groups, job_name):
        self.precincts_graph = Graph.from_json(precincts_graph_path)
        self.state_id = state_id
        self.num_chain_iterations = num_chain_iterations
        self.num_random_districtings = num_random_districtings
        self.precinct_mapping = pd.read_csv(precinct_mapping_path)
        self.output_data_path = output_data_path
        self.population_deviation_threshold = float(population_deviation_threshold)
        self.markov_chain = None
        self.target_groups = target_groups
        self.job_name = job_name

    def create_new_markov_chain(self):
        election = Election("2020_presidential", {"Democratic": "DEMOCRAT", "Republican": "REPUBLICAN"})
        partition_updaters = {
            "2020_presidential": election,
            "total_pop": updaters.Tally("TOTAL_POPULATION", alias="total_pop"),
            "hispanic_pop": updaters.Tally("HISPANIC_LATINO", alias="hispanic_pop"),
            "white_pop": updaters.Tally("WHITE", alias="white_pop"),
            "black_pop": updaters.Tally("AFRICAN_AMERICAN", alias="black_pop"),
            "amer_indian_pop": updaters.Tally("AMERICAN_INDIAN", alias="amer_indian_pop"),
            "asian_pop": updaters.Tally("ASIAN", alias="asian_pop"),
            "pacific_pop": updaters.Tally("PACIFIC_ISLANDER", alias="pacific_pop")
        }

        initial_partition = GeographicPartition(self.precincts_graph, assignment=self.precinct_mapping["0"].to_dict(),
                                                updaters=partition_updaters)

        # compute even population split among every district
        ideal_target_pop = sum(initial_partition["total_pop"].values()) / len(initial_partition)
        # proposal_function that runs every iteration of the chain to evaluate recom with the right constraints
        proposal_function = partial(recom, pop_col="TOTAL_POPULATION", pop_target=ideal_target_pop,
                                    epsilon=self.population_deviation_threshold, node_repeats=20)

        pop_constraint = constraints.within_percent_of_ideal_population(initial_partition,
                                                                        self.population_deviation_threshold,
                                                                        pop_key="total_pop")
        # Markov Chain Initialization
        self.markov_chain = MarkovChain(
            proposal=proposal_function,
            constraints=[pop_constraint],
            accept=accept.always_accept,
            initial_state=initial_partition,
            total_steps=self.num_chain_iterations
        )

    def process_plan_metrics(self, partition):
        num_majority_minority = sw_measures.num_majority_minority_map(partition, self.target_groups)
        num_combined_majority_minority = sw_measures.num_combined_majority_minority(partition, self.target_groups)
        rep_dem_splits = sw_measures.calculate_rep_dem_splits(partition["2020_presidential"])
        polsby_popper_mean = sw_measures.polsby_popper_mean(partition)
        efficiency_gap = sw_measures.efficiency_gap(partition["2020_presidential"])
        seat_vote_points = sw_measures.generate_sv_curve(partition["2020_presidential"])
        box_and_whisker_data = box_and_whisker.calculate_box_and_whisker(partition, self.target_groups, "total_pop")
        row = {"num_majority_minority": num_majority_minority,
               "combined_num_majority_minority": num_combined_majority_minority, "rep_dem_splits": rep_dem_splits,
               "polsby_popper_mean": polsby_popper_mean, "efficiency_gap": efficiency_gap,
               "seat_vote_points": seat_vote_points, "box_and_whisker_data": box_and_whisker_data}
        return row

    def run_chain(self):
        districting_metrics = pd.DataFrame(columns=["num_majority_minority", "combined_num_majority_minority",
                                                    "rep_dem_splits", "polsby_popper_mean", "efficiency_gap",
                                                    "seat_vote_points", "box_and_whisker_data"])
        for i in range(self.num_random_districtings):
            # Run through the iterations of the chain
            self.create_new_markov_chain()
            chain_partition = None
            for idx, chain_partition in enumerate(self.markov_chain):
                pass
            districting_metrics = districting_metrics.append(self.process_plan_metrics(chain_partition), ignore_index=True)

        # Output to output directory
        districting_metrics.to_json(self.output_data_path + "\\random_district_data_"+ self.state_id + "_" + self.job_name +".json", orient="index")


parser = argparse.ArgumentParser(description="Take in config file with paths and other info for MGGG")
parser.add_argument("--config-path", help='path to config json file', required=True)
args = parser.parse_args()
warnings.simplefilter(action='ignore', category=FutureWarning)

with open(args.config_path, "r") as json_file:
    config_info = json.load(json_file)
    json_file.close()

generator = RandomDistrictGenerator(precincts_graph_path=config_info['precincts_graph_path'],
                                    state_id=config_info['state_id'],
                                    num_chain_iterations=config_info['num_chain_iterations'],
                                    num_random_districtings=config_info['num_random_districtings'],
                                    precinct_mapping_path=config_info['precinct_mapping_path'],
                                    output_data_path=config_info["output_data_path"],
                                    population_deviation_threshold=config_info['population_deviation_threshold'],
                                    target_groups=config_info['target_groups'],
                                    job_name=config_info['job_name'])

generator.run_chain()
