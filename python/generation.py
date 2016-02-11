#!/usr/bin/env python
from male import Male
from nest import Nest
from generation_logger import GenerationLogger

from scipy.stats import uniform
import numpy as np
import itertools

# a generation in the model
# aggregates males
# aggregates nest
# steps them through 1 generation of the simulation

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
        
        # first generation no genetics
        if not prev_gen: 
            # create males
            self.searching = [Male(params, self.logger, i) for i in range(params["K"])]
        
        # or create new males based off of the winners in the previous generation    
        else: 
            id_start = 0
            for p in prev_gen.winners:
                self.searching += p.get_offspring(self.params, self.logger, id_start)
                id_start = 1 + self.searching[-1].id

        # remove those that died in the immature phase
        self.searching = filter(lambda m: m.is_alive(), self.searching)
        
        # populate a list of events for each male
        for m in self.searching:
            m.fill_events()

        # sort males by the time of their first event
        self.searching.sort(key = lambda x : x.events[0])

        # step through events 
        self.run()

        # used to grow the next generation, 
        # self.winners is a list of nests that are occupied by males when the females mature
        self.winners = [n for n in self.nests if n.occupied()]
        self.winners = [n for n in self.winners if n.occupier.is_alive()]
        
        if self.params["generation_plot"]:
            self.logger.plot_cohort()

    def run(self):
        f_time = self.params["time_female_maturity"] 
        
        # start the generation when the first male matures:
        self.time =  0

        # until the females mature: 
        while (self.time < f_time):
            if len(self.searching) == 0:
                break
            dt = self.searching[0].events[0] - self.time
            if self.time + dt > f_time:
                break
            chosen = self.searching[0]
            
            # deduct metabolic costs from the chosen male
            chosen.search(self.time + dt)
            
            if not chosen.is_alive(): # either we have died searching or we...
                if self.debug:
                    print "male %s has died at %s" % (chosen.id, self.time)
                self.searching.remove(chosen)
                self.logger.inc_killed()
            else: # attempy to occupy a nest
                self.occupation(chosen, dt)
            
            # re sort the searching list by the first element in the males event list 
            self.searching.sort(key = lambda x : x.events[0])
            
            self.logger.log_cohort()
            self.time += dt

        # final energy deductions for occupiers
        for n in self.nests:
            if n.occupied():
                n.occupier.occupy(f_time)
 
        # final energy deduction for the searchers
        for m in self.searching:
            m.search(f_time, True)
            
        self.logger.log_cohort()

    # chooses a nest and sees if a contest takes place
    def occupation(self, chosen, dt):
        # select a nest a random 
        index = int(uniform.rvs() * len(self.nests))
        nest = self.nests[index]

        if self.debug:
            print "male %s has discovered nest %s at %s" % (
                chosen.id,
                index,
                self.time)

        if nest.occupied():
            self.logger.inc_contests()
            # deduct metabolic costs from the occupier from their last event until now
            nest.occupier.occupy(self.time + dt)

            if self.debug:
                print "\tnest %s is occupied by %s, contest" % (
                    index, 
                    nest.occupier.id)

            loser = nest.contest(chosen)

            # if chosen has won the contest
            # we deal with the loser

            
            if loser != chosen and loser.is_alive():
                self.searching.insert(0, loser)
                self.searching.remove(chosen)
                self.logger.inc_take_overs()
                loser.fill_events(self.time + dt)
            elif not loser.is_alive():
                self.logger.inc_killed()
                if loser == chosen:
                    self.searching.remove(loser)

            if self.debug:
                print "\tnest %s is occupied by %s" % (
                    index, 
                    nest.occupier.id)
        else:
            nest.occupy(chosen)
            self.searching.remove(chosen)
