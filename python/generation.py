##!/usr/bin/env 
from male import Male
from nest import Nest

from scipy.stats import uniform as uni
import numpy as np

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
        # counters:
        self.contests = 0
        self.num_matured = 0
        self.killed = 0

        self.logs = []

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
        self.time = self.immature[0].maturation_time
        self.num_matured += 1
        print "start time\t", self.time
        self.searching.append(self.immature.pop(0))

        # until the females mature: 
        while (self.time < f_time):
            # check next mature male
            if self.immature: # check not null
                if self.immature[0].maturation_time <= self.time:
                    self.searching.append(self.immature.pop(0))
                    self.num_matured += 1
            
            self.time += dt
            
            for m in self.searching:
                # search deducts metabolic costs as well
                if m.search(dt):
                    index = int(uni.rvs()*len(self.nests))
                    # select a nest at random
                    print "male %s has discovered nest %s at %s" % (
                        m.id,
                        index,
                        self.time)
                    nest = self.nests[index]
                    if nest.occupied():
                        print "\tnest %s is occupied by %s, contest" % (
                            index, 
                            nest.occupier.id)
                        print "\tno change"
                        self.contests += 1
                    else:
                        m.occupying = True
                        nest.occupy(m)
                        print "\tnest %s is now occupied by %s" % (
                            index, 
                            m.id)


                if not m.is_alive():
                    print "male %s has died at %s" % (m.id, self.time)

            # remove dead searching males
            self.killed += len(self.searching)
            self.searching = filter(lambda m: m.is_alive(), self.searching) 
            self.killed -= len(self.searching)

            # remove occupying males
            self.searching = filter(lambda m: not m.occupying, self.searching)
            
            self.log_cohort()
        
        self.plot_cohort()


            # occupying

    # logs stats about the cohort to a list
    def log_cohort(self):
        row = dict()
        # average energy of searching males
        # number occupied
        # number searching 
        row["time"] = self.time
        row["searching"] = len(self.searching) 
        row["contests"] = self.contests 
        row["num_matured"] = self.num_matured
        row["killed"] = self.killed
        print row
        self.logs.append(row)

    def plot_cohort(self):
        
        # these lambdas get the values from the object
        get_energy = lambda x: x.energy
        get_mass = lambda x: x.mass
        get_m_time = lambda x: x.maturation_time

        times = [ row["time"] for row in self.logs ]
        searching = [ row["searching"] for row in self.logs ]
        contests = [ row["contests"] for row in self.logs ]
        num_matured = [ row["num_matured"] for row in self.logs ]
        killed = [ row["killed"] for row in self.logs ]

        plt.plot(times, searching, label = "searching males")
        plt.plot(times, contests, label = "total contests")
        plt.plot(times, num_matured, label = "total matured")
        plt.plot(times, killed, label = "total_deaths")
        plt.legend(loc = 2)

        plt.show()