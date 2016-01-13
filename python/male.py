#!/usr/bin/python

import math
from scipy.stats import norm, logistic

# a male individual in the population
class Male(object):
    #TODO
    """
        qualities:
            @maturation time:
            @energy at maturation
            @mass at maturation
        
        heriditable traits:
            @exploration 
            psi
            aggression

        costs:
            metabolic
            predation

        events:
            contests
            searching
            abandoning

        genetics:
            ?????????
            ?????????
            ?????????
    """


    # constructor
    def __init__(self, params, id, mom = None, dad = None):
        self.id = id
        if not mom and not dad: # first gen no breeding

            # pull the exploration trait from the normal distrobution
            self.exploration = abs(norm.rvs(
                params["exploration_mean"],
                params["exploration_sd"]))

            # countdown timer to next event
            self.tt_event = self.exploration
            
            self.metabolic_cost_search = params["metabolic_cost_search"]
            self.metabolic_cost_occupy = params["metabolic_cost_occupy"]
            
            # pull the maturation time from the inverse logit
            self.maturation_time = abs(logistic.rvs(
                params["maturation_center"],
                params["maturation_width"]))

            #get mass at maturation:
            self.grow(params)

            # energy at maturation
            self.energy = self.mass * params["mass_to_energy"]
        else:
            # gentetic breeding 
            # TODO
            pass
    
    # mass from 0 to time t
    def grow(self, params):
        a = params["growth_param_a"]
        b = params["growth_param_b"]
        self.mass =  pow(params["initial_mass"], 1.0 - b) 
        self.mass += self.maturation_time * a * ( 1.0 - b )
        self.mass = pow(self.mass, 1.0/(1.0 - b))
    
    # a male explores its surroundings
    # returns true if the male has discovered a nest
    # false if otherwise
    def search(self, dt):
        self.tt_event -= dt
        self.energy -= dt * self.metabolic_cost_search
        if self.tt_event <= 0:
            self.tt_event = self.exploration
            return True
        else:
            return False


    # the outcome of a contest is decided here
    def contest(self, opponent):
        pass

    def is_alive(self):
        return self.energy > 0

    def to_string(self):
        return "%s:explor = %s\tm_time = %s\tM = %s\tE = %s" % (
            self.id,
            self.exploration,
            self.maturation_time,
            self.mass,
            self.energy)