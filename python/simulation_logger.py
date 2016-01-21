import numpy as np
import matplotlib.pyplot as plt
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
            "num_winners": []
        }

    def log(self, gen):
        winning_males = [ n.occupier for n in gen.winners ]

        exploration_traits = map(lambda x: x.exploration_trait, winning_males)

        aggro_traits = map(lambda x: x.aggro, winning_males)

        self.data["generation"].append(gen.id)
        self.data["mean_exploration"].append(np.mean(exploration_traits))
        self.data["std_exploration"].append(np.std(exploration_traits))
        self.data["mean_aggro"].append(np.mean(aggro_traits))
        self.data["std_aggro"].append(np.std(aggro_traits))
        self.data["num_winners"].append(len(winning_males))

    # TODO
    def print_csv(self):
        pass

    # TODO I need some way to match the paramters with a plot
    def plot(self):
        gens = self.data["generation"]
        
        plt.plot(gens, self.data["mean_exploration"], label = "mean exploration")
        plt.plot(gens, self.data["std_exploration"], label = "std exploration")
        plt.plot(gens, self.data["mean_aggro"], label = "mean aggro")
        plt.plot(gens, self.data["std_aggro"], label = "std aggro")

        plt.legend(loc = 2)
        plt.title("Trait values through Generations")
        
        plt.xlabel("generation")
        plt.ylabel("value")

        plt.show()

