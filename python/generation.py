##!/usr/bin/env 
from male import Male
from nest import Nest

from scipy.stats import uniform as uni

import matplotlib.pyplot as plt

# a generation in the minimal model
# aggregates males
# aggregates nests
# steps them through 1 generation of the simulation

# TODO: 
# step directly to next event not through time_steps
# nest collisions (this shouldn't be an issue for small deltas)

class Generation:

    # constructor
    # params is the parameter dict
    # prev gen is the previous generation of creatures
    def __init__(self, params, prev_gen=None):
        self.params = params

        if not prev_gen: # no genetics
            # initialise some lists
            self.searching = []
            # create males
            self.immature = [Male(params, i) for i in range(params["K"])]
            # sort males by when they mature
            self.immature.sort(key = lambda x : x.maturation_time)

            # make nests
            self.nests = [Nest(params, i) for i in range(params["N"])]
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
                    # select a nest at random
                    index = int(uni.rvs()*len(self.nests))
                    print "male %s has discovered nest %s at %s" % (
                        m.id,
                        index,
                        time)
                if not m.is_alive():
                    print "male %s has died at %s" % (m.id, time)


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