#!/usr/bin/env python

import json
import numpy as np
from generation import Generation


# the simulation class aggregates generation objects
class Simulation(object):

    # constructor
    def __init__(self, params):
        self.params = params
        self.generations = list()
        self.current_gen = 0

    # creates the next generation from the previous one
    def step(self):
        if self.current_gen > 0:
            self.generations.append(Generation(
                self.params,
                prev_gen = self.generations[-1],
                id = self.current_gen))
            # remove the second last generation from memory so we dont blow out
            del self.generations[-2]
        else:
            self.generations.append(Generation(
                self.params,
                id = self.current_gen))
        self.current_gen += 1


def main():
    # read in parameters from file

    params = json.loads(open("parameters.json").read())
    np.random.seed(seed=params["random_seed"])
    
    sim = Simulation(params)
    for i in range(params["generations"]):
        print ""
        print "gen", i
        sim.step()
        if i % params["save_every"] == 0 and params["save_scatter_pngs"]:
            sim.generations[-1].logger.plot_trait_scatter(True)
        
        if i % params["save_every"] == 0 and params["save_energy_pngs"]:
            sim.generations[-1].logger.plot_e_time_series(True)

        print "num winners: ",len(sim.generations[-1].winners)

    if params["final_plot"]:
        sim.generations[-1].logger.plot_cohort()

if __name__ == '__main__':
    main()