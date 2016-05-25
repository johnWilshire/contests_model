import numpy as np
import matplotlib.pyplot as plt
import uuid
from time import gmtime, strftime
import json

"""
    This class holds summary information about the generations in a simulation
"""
class SimulationLogger (object):
    def __init__(self, simulation, params):
        self.simulation = simulation
        self.params = params
        self.data = {
            "generation":[],
            "mean_exploration":[],
            "std_exploration":[],
            "mean_e_0":[],
            "std_e_0":[],
            "mean_k":[],
            "std_k":[],
            "mean_maturation":[],
            "std_maturation":[],
            "num_winners":[],
            "contest_energy":[],
            "search_energy":[],
            "occupying_energy":[]
        }


        self.winners = {
            "generation":[],
            "e_0":[],
            "k":[],
            "speed":[],
            "radius":[],
            "maturation_t1ime":[],
            "mass":[],
            "energy_at_female_maturity":[]
        }

        # log the traits of individuals with a nest at the end of each generation:


    def log(self, gen):
        winning_males = [ n.occupier for n in gen.winners ]

        exploration_traits = map(lambda x: x.exploration, winning_males)
        aggression_e_0_traits = map(lambda x: x.e_0, winning_males)
        aggression_k_traits = map(lambda x: x.k, winning_males)
        maturations = map(lambda x: x.maturation_time, winning_males)


        self.data["generation"].append(gen.id)
        self.data["mean_exploration"].append(np.mean(exploration_traits))
        self.data["std_exploration"].append(np.std(exploration_traits))
        self.data["mean_e_0"].append(np.mean(aggression_e_0_traits))
        self.data["std_e_0"].append(np.std(aggression_e_0_traits))
        self.data["mean_k"].append(np.mean(aggression_k_traits))
        self.data["std_k"].append(np.std(aggression_k_traits))
        self.data["mean_maturation"].append(np.mean(maturations))
        self.data["std_maturation"].append(np.std(maturations))
        self.data["num_winners"].append(len(winning_males))

        #the energy data
        self.data["contest_energy"].append(gen.logger.data["contest_energy"][-1])
        self.data["search_energy"].append(gen.logger.data["search_energy"][-1])
        self.data["occupying_energy"].append(gen.logger.data["occupying_energy"][-1])

        if gen.id % self.params["log_traits_every"] == 0:
            for male in winning_males:
                self.winners["generation"].append(gen.id)
                self.winners["e_0"].append(male.e_0)
                self.winners["k"].append(male.k)
                self.winners["speed"].append(male.speed)
                self.winners["radius"].append(male.radius)
                self.winners["maturation_t1ime"].append(male.maturation_time)
                self.winners["mass"].append(male.mass)
                self.winners["energy_at_female_maturity"].append(male.energy)
            

        if self.params["debug"]:
            print "contest_energy:", generation["contest_energy"]
            print "search_energy: ", generation["search_energy"]
            print "occupying_energy:", generation["occupying_energy"]


    def log_traits_to_JSON_file(self):
        # the json that we will write to file to read later in R
        jsons = {
            "parameters":self.params,
            "traits":self.winners,
            "history":self.data,
            "contests":self.simulation.generations[-1].logger.contest_data
        }

        file_name = "../data/" + strftime("%m_%d_%H_%M_%S__", gmtime()) + str(uuid.uuid4()) + ".json"
        
        f = open(file_name,"w")
        f.write(json.dumps(jsons))
        f.close()


    # returns true if the early exit conditions have been met
    def get_early_exit(self):
        if self.data["generation"][-1] >  self.params["min_gen"]:
            lag_length = self.params["stability_lag"]
            # finds the max sd of the traits in the last 'lag' generations

            delta = lambda x: max(x[ -lag_length:]) - min(x[ -lag_length:])

            max_delta = max( 
                delta(self.data["std_e_0"]),
                delta(self.data["mean_e_0"]),
                delta(self.data["std_k"]),
                delta(self.data["mean_k"]),
                delta(self.data["mean_exploration"])
            )

            if self.params["debug"]:
                print "max delta: %s" % max_delta

            if max_delta < self.params["stability_cutoff"]:
                return True
        return False
        
    def plot(self, savefig = False):

        gens = self.data["generation"]
        

        plt.plot(gens, [ g["mean_exploration"] for g in self.data ], label = "mean exploration")
        plt.plot(gens, [ g["std_exploration"] for g in self.data ], label = "std exploration")
        plt.plot(gens, [ g["mean_e_0"] for g in self.data ], label = "mean e_0")
        plt.plot(gens, [ g["std_e_0"] for g in self.data ], label = "std e_0")
        plt.plot(gens, [ g["mean_k"] for g in self.data ], label = "mean k")
        plt.plot(gens, [ g["std_k"] for g in self.data ], label = "std k")
        plt.plot(gens, [ g["mean_maturation"] for g in self.data ], label = "mean maturationtime")
        plt.plot(gens, [ g["std_maturation"] for g in self.data ], label = "std maturation_time")
        
        g.legend(loc = 2)
        plt.title("Trait values through Generations")
        
        plt.xlabel("generation")
        plt.ylabel("value")

        if savefig:
            plt.savefig("plots/gen_simulation_trait_values.png" % self.generation.id)
            plt.close()
            return
        plt.show()

