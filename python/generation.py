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
        i = 0
        while (self.time < f_time):
            i += 1

            # check next mature male
            if self.immature: # check not null
                if self.immature[0].maturation_time <= self.time:
                    self.searching.append(self.immature.pop(0))
                    self.num_matured += 1
            
            
            # iterate over nests subtracting metabolic costs from occupying males
            for n in self.nests:
                if n.occupied():
                    n.occupier.occupy(dt)
                    if not n.occupier.is_alive(): # remove the dead
                        m = n.eject()
                        self.killed += 1
                        print "%s, male %s in nest %s has died at t = %s" % ( i,
                            m.id,
                            n.id,
                            self.time)


            # iterate over searching males
            self.searching_step(dt)

            self.log_cohort()

            self.time += dt
        
        self.plot_cohort()


            # occupying

    # itereates over all searching males
    def searching_step(self, dt):
        for m in self.searching[:]:
            if not m.is_alive():
                print "male %s has died at %s" % (m.id, self.time)
                self.searching.remove(m)
                self.killed += 1
            elif m.search(dt):
                # select a nest at randoms
                index = int(uni.rvs() * len(self.nests))
                print "male %s has discovered nest %s at %s" % (
                    m.id,
                    index,
                    self.time)
                nest = self.nests[index]
                if nest.occupied():
                    print "\tnest %s is occupied by %s, contest" % (
                        index, 
                        nest.occupier.id)
                    loser = nest.contest(m)
                    if loser.id != m.id:
                        self.searching.insert(0,loser)
                        self.searching.remove(m)
                    self.contests += 1
                    print "\tnest %s is occupied by %s" % (
                        index, 
                        nest.occupier.id)

                else:
                    nest.occupy(m)
                    self.searching.remove(m)
                    print "\tnest %s is now occupied by %s" % (
                        index, 
                        m.id)

        # remove occupying males
        self.searching = filter(lambda m: not m.occupying, self.searching) 
        # remove dead males
        self.killed += len(self.searching)
        self.searching = filter(lambda m: m.is_alive(), self.searching) 
        self.killed -= len(self.searching)

    # logs stats about the cohort to a list
    def log_cohort(self):
        row = dict()
        # average energy of searching males
        row["time"] = self.time
        row["searching"] = len(self.searching)
        row["occupying"] = len(filter(lambda n: n.occupied(), self.nests))
        row["contests"] = self.contests 
        row["num_matured"] = self.num_matured
        row["killed"] = self.killed

        row["energy_searching"] = np.mean([m.energy for m in self.searching])
        row["energy_occupying"] = np.mean([n.occupier.energy 
                                            for n in self.nests
                                                if n.occupied()])
        self.logs.append(row)

    def get_col(self, col_name):
        return [ row[col_name] for row in self.logs ]

    def plot_cohort(self):
        
        # these lambdas get the values from the object
        get_energy = lambda x: x.energy
        get_mass = lambda x: x.mass
        get_m_time = lambda x: x.maturation_time

        times = self.get_col("time")
        searching = self.get_col("searching")
        occupying = self.get_col("occupying")
        contests = self.get_col("contests")

        num_matured = self.get_col("num_matured")
        killed = self.get_col("killed")
        
        mean_energy_searching = self.get_col("energy_searching")
        mean_energy_occupying = self.get_col("energy_occupying")

        plt.title("various metrics through time")
        plt.xlabel("time steps")
        plt.plot(times, searching, label = "searching males")
        plt.plot(times, occupying, label = "occupying males")
        plt.plot(times, contests, label = "total contests")
        plt.plot(times, num_matured, label = "total matured")
        plt.plot(times, killed, label = "total_deaths")
        plt.legend(loc = 2)
        plt.show()
        
        plt.title("Mean energy levels through time")
        plt.xlabel("time steps")
        plt.ylabel("mean Energy values (J)")
        plt.plot(times, mean_energy_searching, label = "searching")
        plt.plot(times, mean_energy_occupying, label = "occupying")
        plt.legend(loc = 2)
        plt.show()


        occupying_males = [ n.occupier for n in self.nests if n.occupied()]
        occupying_exploration_trait = [m.exploration for m in occupying_males]
        occupying_aggro_trait = [m.aggro / self.params["aggression_max"] for m in occupying_males]
        
        bins = np.linspace(-10, 10, )
        plt.hist(occupying_exploration_trait, self.params["trait_bins"], alpha = 0.5, label = "exploration")
        plt.hist(occupying_aggro_trait, self.params["trait_bins"], alpha = 0.75, label = "aggression")
        plt.legend(loc = 2)
        plt.show()
        

        plt.plot(occupying_exploration_trait, occupying_aggro_trait, 'ro')
        plt.title("trait values of individuals")
        plt.xlabel("exploration")
        plt.ylabel("aggression")
        plt.show()