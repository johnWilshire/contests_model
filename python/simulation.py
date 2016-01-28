#!/usr/bin/env python

import json
import numpy as np
import sys
from generation import Generation
from simulation_logger import SimulationLogger

# the simulation class aggregates generation objects
class Simulation(object):

    # constructor
    def __init__(self, params):
        self.params = params
        self.generations = []
        self.logger = SimulationLogger(self, params)
        self.current_gen = 0

    # creates the next generation from the previous one
    def step(self):
        if self.current_gen > 0:
            self.generations.append(Generation(
                self.params,
                prev_gen = self.generations[-1],
                id = self.current_gen))

            # remove the second last generation from memory 
            # so we dont blow out
            del self.generations[-2]
        else:
            self.generations.append(Generation(
                self.params,
                id = self.current_gen))
        
        self.logger.log(self.generations[-1])
        
        self.current_gen += 1


def main():
    # read in default parameters from file

    params = json.loads(open("parameters.json").read())

    # overwrite a specified parameter from arguments
    if len(sys.argv) == 3:
        p = sys.argv[1]
        # type conversion
        params[p] = type(params[p])(sys.argv[2])

    np.random.seed(seed=params["random_seed"])
    
    sim = Simulation(params)
    for i in range(params["generations"]):
        print ""
        print "gen =\t\t", i
        print "patch area = \t", params["patch_area"]
        sim.step()
        if i % params["save_every"] == 0:
            if params["save_scatter_pngs"]:
                sim.generations[-1].logger.plot_trait_scatter(True)
            if params["save_energy_pngs"]:
                sim.generations[-1].logger.plot_e_time_series(True)
            if params["save_time_series_pngs"]:
                sim.generations[-1].logger.plot_time_series(True)

        print "num winners =\t",len(sim.generations[-1].winners)

    if params["final_plot"]:
        sim.logger.plot(params["save_sim_trait_pngs"])
        sim.generations[-1].logger.plot_cohort()

    if params["sim_plot"]:
        sim.logger.plot(params["save_sim_trait_pngs"])

    if params["simulation_log_to_file"]:
        sim.logger.log_traits_to_JSON_file()

if __name__ == '__main__':
    main()