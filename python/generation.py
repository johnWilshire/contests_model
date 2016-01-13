##!/usr/bin/env 
from male import Male
from nest import Nest

import matplotlib.pyplot as plt

# a generation in the minimal model
# aggregates males
# aggregates nests
# steps them through 1 generation of the simulation

# TODO: step directly to next event not through time_steps

class Generation:

    # constructor
    # params is the parameter dict
    # prev gen is the previous generation of creatures
    def __init__(self, params, prev_gen=None):
        self.params = params

        if not prev_gen:
            # initialise some lists
            self.immature = []
            self.searching = []
            self.unoccupied_nests = []
            self.occupied_nests = []

            # create males
            self.immature = [Male(params, i) for i in range(params["K"])]

            # sort males by when they mature
            self.immature.sort(key = lambda x : x.maturation_time)

            # pull from a range of RR's for nests
            self.unoccupied_nests = [Nest(params, i) for i in range(params["N"])]
        else:
            # TODO
            # some genetics stuff here xD
            pass

        self.run()
        # for each male increment exploration by their lambda
        # when exploration reaches some value
        # pick a nest and occupy or contest

    def run(self):
        dt = self.params["time_step"]
        f_time = self.params["time_female_maturity"]

        # print the cohort
        for x in self.immature:
            print x.to_string() 
        
        # start the generation when the first male matures:
        time = self.immature[0].maturation_time
        print "start time\t", time
        self.searching.append(self.immature.pop(0))

        # until the females mature: 
        while (time < f_time):
            # check next mature male
            if self.immature: # check not null
                if self.immature[0].maturation_time >= time:
                    self.searching.append(self.immature.pop(0))
            
            # searching males search
            # remove dead searching males
            self.searching = filter(lambda m: m.is_alive(), self.searching) 
            
            time += dt
            for m in self.searching:
                if m.search(dt):
                    print "male %s has discovered a nest at" % m.id, time
                if not m.is_alive():
                    print "male %s has died at " % m.id, time


            # occupying



    def plot_cohort(self):
        
        # these lambdas get the values from the object
        get_energy = lambda x: x.energy
        get_mass = lambda x: x.mass
        get_m_time = lambda x: x.maturation_time


        plt.plot(map(get_energy, self.immature), label = "energy")
        plt.plot(map(get_mass, self.immature), label = "mass")
        plt.plot(map(get_m_time, self.immature), label = "maturation time")
        plt.legend(loc = 2)

        plt.show()