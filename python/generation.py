#!/usr/bin/env python
from male import Male
from nest import Nest
from generation_logger import GenerationLogger

from scipy.stats import uniform
import numpy as np

# a generation in the minimal model
# aggregates males
# aggregates nest
# steps them through 1 generation of the simulation

# TODO: 
# step directly to next event not through time_steps
# mature based off mass logistic pdf???

class Generation (object):

    # constructor
    # params is the parameter dict
    # prev gen is the previous generation of creatures
    def __init__(self, params, prev_gen=None, id=0):
        self.params = params
        self.id = id
        # counters:
        self.debug = params["debug"]
        self.logger = GenerationLogger(self)
        
        # make nests
        self.nests = [Nest(params, i) for i in range(params["N"])]

        self.searching = []


        if not prev_gen: # no genetics
            # create males
            self.immature = [Male(params, self.logger, i) for i in range(params["K"])]
            
        else: # previous generation
            self.immature = []
            id_start = 0
            for p in prev_gen.winners:
                self.immature += p.get_offspring(self.params, self.logger, id_start)
                id_start = 1 + self.immature[-1].id

            if self.debug:
                print "next generation has %s individuals" % len(self.immature)

        # sort males by when they mature
        self.immature.sort(key = lambda x : x.maturation_time)
        self.run()
        if self.params["generation_plot"]:
            self.logger.plot_cohort()

        self.winners = [n for n in self.nests if n.occupied()]

    def run(self):
        dt = self.params["time_step"]
        f_time = self.params["time_female_maturity"]

        # print the cohort
        if self.debug:
            for x in self.immature:
                print x.to_string() 
        
        # start the generation when the first male matures:
        self.time = self.immature[0].maturation_time
        self.logger.inc_num_matured()
        if self.debug:
            print "start time\t", self.time

        self.searching.append(self.immature.pop(0))

        # until the females mature: 
        while (self.time < f_time):
            # check the next mature male
            self.maturation_step()
            # iterate over occupying males
            self.occupation_step(dt)
            # iterate over searching males
            self.searching_step(dt)
            self.logger.log_cohort()
            self.time += dt


    # itereates over all searching males
    def searching_step(self, dt):
        # iterate over a copy of the searching male list so we can add
        # and remove males from it
        for m in self.searching[:]: 
            discovered =  m.search(dt)
            if not m.is_alive():
                if self.debug:
                    print "male %s has died at %s" % (m.id, self.time)
                self.searching.remove(m)
                self.logger.inc_killed()
                self.logger.dec_searching()
            elif discovered:
                # select a nest at random
                index = int(uniform.rvs() * len(self.nests))
                nest = self.nests[index]

                if self.debug:
                    print "male %s has discovered nest %s at %s" % (
                        m.id,
                        index,
                        self.time)
                    
                if nest.occupied():
                    self.logger.inc_contests()

                    if self.debug:
                        print "\tnest %s is occupied by %s, contest" % (
                            index, 
                            nest.occupier.id)

                    loser = nest.contest(m)
                    if loser.id != m.id:
                        self.searching.insert(0,loser)
                        self.searching.remove(m)
                        self.logger.inc_take_overs()

                    if self.debug:
                        print "\tnest %s is occupied by %s" % (
                            index, 
                            nest.occupier.id)

                # un occupied nests are taken over by the searching male
                else:
                    nest.occupy(m)
                    self.searching.remove(m)
                    self.logger.inc_occupying()
                    self.logger.dec_searching()

                    if self.debug:
                        print "\tnest %s is now occupied by %s" % (
                            index, 
                            m.id)

    # allows males to mature
    def maturation_step(self):
        maturing = filter(lambda m: m.maturation_time <= self.time, self.immature)
        for m in maturing:
            self.searching.append(m)
            self.immature.remove(m)
            if self.debug:
                print "male matured at %s" % self.time
            self.logger.inc_num_matured()
            self.logger.inc_searching()

    # iterate over nests subtracting metabolic costs from occupying
    # males
    def occupation_step(self, dt):
        for n in self.nests:
            if n.occupied():
                n.occupier.occupy(dt)
                if not n.occupier.is_alive(): # remove the dead males
                    m = n.eject()
                    self.logger.inc_killed()
                    self.logger.dec_occupying()
                    if self.debug:
                        print "male %s in nest %s has died at t = %s" % (
                            m.id,
                            n.id,
                            self.time)
