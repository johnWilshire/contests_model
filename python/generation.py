#!/usr/bin/env python
from male import Male
from nest import Nest
from logger import Logger

from scipy.stats import uniform

# a generation in the minimal model
# aggregates males
# aggregates nests
# steps them through 1 generation of the simulation

# TODO: 
# step directly to next event not through time_steps
# move logs into a new class

class Generation (object):

    # constructor
    # params is the parameter dict
    # prev gen is the previous generation of creatures
    def __init__(self, params, prev_gen=None):
        self.params = params
        # counters:
        self.contests = 0
        self.num_matured = 0
        self.killed = 0
        self.debug = params["debug"]

        self.logger = Logger(self)

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

    def run(self):
        dt = self.params["time_step"]
        f_time = self.params["time_female_maturity"]

        # print the cohort
        if self.debug:
            for x in self.immature:
                print x.to_string() 
        
        # start the generation when the first male matures:
        self.time = self.immature[0].maturation_time
        self.num_matured += 1
        if self.debug:
            print "start time\t", self.time

        self.searching.append(self.immature.pop(0))
        step = 0
        # until the females mature: 
        while (self.time < f_time):
            step += 1
            # check the next mature male
            maturing = filter(lambda m: m.maturation_time <= self.time, self.immature)
            for m in maturing:
                self.searching.append(m)
                self.immature.remove(m)
                if self.debug:
                    print "male matured at %s" % self.time
                self.num_matured += 1
            
            
            # iterate over nests subtracting metabolic costs from occupying
            # males
            self.occupying = 0
            for n in self.nests:
                if n.occupied():
                    n.occupier.occupy(dt)
                    if not n.occupier.is_alive(): # remove the dead males
                        m = n.eject()
                        self.killed += 1
                        if self.debug:
                            print "male %s in nest %s has died at t = %s" % (
                                m.id,
                                n.id,
                                self.time)
                    else:
                        self.occupying += 1


            # iterate over searching males
            self.searching_step(dt)

            self.logger.log_cohort()

            self.time += dt
        
        if self.params["generation_plot"]:
            self.logger.plot_cohort()

    # itereates over all searching males
    def searching_step(self, dt):
        # iterate over a copy of the searching male list so we can add
        # and remove males from it
        for m in self.searching[:]: 
            if not m.is_alive():
                if self.debug:
                    print "male %s has died at %s" % (m.id, self.time)
                self.searching.remove(m)
                self.killed += 1

            elif m.search(dt):
                # select a nest at random
                index = int(uniform.rvs() * len(self.nests))
                if self.debug:
                    print "male %s has discovered nest %s at %s" % (
                        m.id,
                        index,
                        self.time)
                nest = self.nests[index]
                if nest.occupied():
                    if self.debug:
                        print "\tnest %s is occupied by %s, contest" % (
                            index, 
                            nest.occupier.id)
                    loser = nest.contest(m)
                    if loser.id != m.id:
                        self.searching.insert(0,loser)
                        self.searching.remove(m)
                    self.contests += 1
                    if self.debug:
                        print "\tnest %s is occupied by %s" % (
                            index, 
                            nest.occupier.id)
                # un occupied nests are taken over by the searching male
                else:
                    nest.occupy(m)
                    self.occupying += 1
                    self.searching.remove(m)
                    if self.debug:
                        print "\tnest %s is now occupied by %s" % (
                            index, 
                            m.id)

