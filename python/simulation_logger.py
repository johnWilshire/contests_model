import numpy as np
import matplotlib.pyplot as plt
import uuid
from time import gmtime, strftime
import json

"""
    This class will hold summary information about many generations in a simulation
"""
class SimulationLogger (object):
    def __init__(self, simulation, params):
        self.simulation = simulation
        self.params = params
        self.data = {
            "generation": [],
            "mean_exploration": [],
            "std_exploration": [],
            "mean_aggro": [],
            "std_aggro": [],
            "mean_maturation":[],
            "std_maturation":[],
            "contest_energy":[],
            "search_energy":[],
            "occupying_energy":[],
            "num_winners": []
        }

    def log(self, gen):
        winning_males = [ n.occupier for n in gen.winners ]

        exploration_traits = map(lambda x: x.exploration, winning_males)

        aggro_traits = map(lambda x: x.aggro, winning_males)

        maturations = map(lambda x: x.maturation_time, winning_males)

        self.data["generation"].append(gen.id)
        self.data["mean_exploration"].append(np.mean(exploration_traits))
        self.data["std_exploration"].append(np.std(exploration_traits))
        self.data["mean_aggro"].append(np.mean(aggro_traits))
        self.data["std_aggro"].append(np.std(aggro_traits))
        self.data["mean_maturation"].append(np.mean(maturations))
        self.data["std_maturation"].append(np.std(maturations))
        self.data["num_winners"].append(len(winning_males))

        #get the energy data
        
        self.data["contest_energy"].append(
            gen.logger.data["contest_energy"][-1]
        )
        self.data["search_energy"].append(
            gen.logger.data["search_energy"][-1]
        )
        self.data["occupying_energy"].append(
            gen.logger.data["occupying_energy"][-1]
        )


    def  log_traits_to_JSON_file(self):
        # get the winners
        winners = self.simulation.generations[-1].winners
        winners = [ n.occupier for n in winners ]

        traits = []

        for male in winners:
            m = {}
            m["aggression"] = male.aggro
            m["speed"] = male.speed
            m["radius"] = male.radius
            m["maturation_time"] = male.maturation_time
            m["mass"] = male.mass
            m["energy_at_female_maturity"] = male.energy

            traits.append(m)
        # the json that we will write to file
        jsons = {
            "parameters":self.params,
            "traits":traits,
            "history":self.data
        }

        file_name = "data/" + strftime("%m_%d_%H_%M_%S__", gmtime()) + str(uuid.uuid4()) + ".json"
        
        f = open(file_name,"w")
        f.write(json.dumps(jsons))
        f.close()

    # returns true if the early exit conditions have been met

    def get_early_exit(self):
        last_aggro = self.data["std_aggro"][-1]
        last_exploration = self.data["std_exploration"][-1]
        print "std's of traits exp %s, aggression %s" % (last_exploration, last_aggro)
        cutoff = self.params["early_exit_sd_cutoff"]
        if last_aggro < cutoff and last_exploration < cutoff:
            if self.data["num_winners"][-1] > self.params["min_winners_cutoff"]:
                return True
        return False
        

    def plot(self, savefig = False):
        gens = self.data["generation"]
        
        plt.plot(gens, self.data["mean_exploration"], label = "mean exploration")
        plt.plot(gens, self.data["std_exploration"], label = "std exploration")
        plt.plot(gens, self.data["mean_aggro"], label = "mean aggro")
        plt.plot(gens, self.data["std_aggro"], label = "std aggro")

        plt.plot(gens, self.data["mean_maturation"], label = "mean maturationtime")
        plt.plot(gens, self.data["std_maturation"], label = "std maturation_time")

        plt.legend(loc = 2)
        plt.title("Trait values through Generations")
        
        plt.xlabel("generation")
        plt.ylabel("value")

        if savefig:
            plt.savefig("plots/gen_simulation_trait_values.png" % self.generation.id)
            plt.close()
            return
        plt.show()

