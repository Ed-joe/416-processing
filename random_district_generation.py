import argparse
import json
from functools import partial
from gerrychain import (GeographicPartition, Graph, MarkovChain, updaters, constraints, accept, Election)
from gerrychain.proposals import recom


class RandomDistrictGenerator:
    def __init__(self, precincts_data_path, state_id, num_chain_iterations, num_random_districtings,
                 precinct_mapping_column_id, initial_partition_path, output_data_path, population_deviation_threshold):
        self.precincts_data_path = precincts_data_path
        self.state_id = state_id
        self.num_chain_iterations = num_chain_iterations
        self.num_random_districtings = num_random_districtings
        self.precinct_mapping_column_id = precinct_mapping_column_id
        self.output_data_path = output_data_path
        self.population_deviation_threshold = population_deviation_threshold
        self.initial_partition = None
        self.precincts_graph = Graph.from_file(precincts_data_path)
        self.markov_chain = None

    def create_new_markov_chain(self):
        election = Election("2020_presidential", {"Democratic": "2020_biden_votes", "Republican": "2020_trump_votes"})
        partition_updaters = {
            "2020_presidential": election,
            "total_pop": updaters.Tally("total_pop"),
            "hispanic_pop": updaters.Tally("hispanic_pop"),
            "white_pop": updaters.Tally("white_pop"),
            "black_pop": updaters.Tally("black_pop"),
            "amer_indian_pop": updaters.Tally("amer_indian_pop"),
            "asian_pop": updaters.Tally("asian_pop"),
            "pacific_pop": updaters.Tally("pacific_pop"),
            "other_pop": updaters.Tally("other_pop"),
            "two_or_more_pop": updaters.Tally("two_or_more_pop")
        }

        self.initial_partition = GeographicPartition(self.precincts_graph, assignment=self.precinct_mapping_column_id,
                                                     updaters=partition_updaters)

        # compute even population split among every district
        ideal_target_pop = sum(self.initial_partition["total_pop"].values()) / len(self.initial_partition)
        # proposal_function that runs every iteration of the chain to evaluate recom with the right constraints
        proposal_function = partial(recom, pop_col="total_pop", pop_target=ideal_target_pop,
                                    epsilon=self.population_deviation_threshold, node_repeats=2)

        pop_constraint = constraints.within_percent_of_ideal_population(self.initial_partition,
                                                                        self.population_deviation_threshold)
        # Markov Chain Initialization
        self.markov_chain = MarkovChain(
            proposal=proposal_function,
            constraints=[pop_constraint],
            accept=accept.always_accept,
            initial_state=self.initial_partition,
            total_steps=self.num_chain_iterations
        )

    def run_chain(self):
        for i in range(self.num_random_districtings):
            self.create_new_markov_chain()
            # Run through the iterations of the chain
            chain_partition = None
            for idx, chain_partition in enumerate(self.markov_chain):
                pass

        # TODO Post Process the new random district plans


parser = argparse.ArgumentParser(description="Take in config file with paths and other info for MGGG")
parser.add_argument("--config-path", help='path to config json file', required=True)
args = parser.parse_args()

with open(args.config_path, "r") as jsonfile:
    config_info = json.load(jsonfile)
    jsonfile.close()

generator = RandomDistrictGenerator(precincts_data_path=config_info['precincts_data_path'],
                                    state_id=config_info['state_id'],
                                    num_chain_iterations=config_info['num_chain_iterations'],
                                    num_random_districtings=config_info['num_random_districtings'],
                                    precinct_mapping_column_id=config_info['precinct_mapping_column_id'],
                                    output_data_path=config_info["output_data_path"],
                                    population_deviation_threshold=config_info['population_deviation_threshold'])
