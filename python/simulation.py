#!/usr/bin/python

import json
import numpy as np
from generation import Generation


# the simulation class aggregates generation objects
class Simulation:

    # constructor
    def __init__(self, params):
        self.params = params
        self.generations = list()
        self.current_gen = 0

    # makes the first generation
    def start(self):
        self.current_gen += 1
        self.generations.append(Generation(self.params))

    # creates the next generation from the previous one
    def step(self):
        self.current_gen += 1
        self.generations.append(Generation(
            self.params,
            prev_gen = self.generations[-1],
            id = self.current_gen))

def main():
    # read in parameters from file

    params = json.loads(open("parameters.json").read())
    np.random.seed(seed=params["random_seed"])
    # create a new simulation object

    sim = Simulation(params)
    sim.start()
    if params["initial_plot"]:
        sim.generations[0].logger.plot_cohort()
    for i in range(1, params["generations"]):
        sim.step()

    if params["final_plot"]:
        sim.generations[0].logger.plot_cohort()

if __name__ == '__main__':
    main()