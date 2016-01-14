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
        self.generations.append(Generation(self.params))
        self.current_gen += 1

    # creates the next generation from the previous one
    def step(self):
        prev_gen = generations[-1]
        self.generations.append(Generation(prev_gen))
        self.current_gen += 1

def main():
    # read in parameters from file

    params = json.loads(open("parameters.json").read())
    np.random.seed(seed=params["random_seed"])
    # create a new simulation object

    sim = Simulation(params)
    sim.start()

if __name__ == '__main__':
    main()