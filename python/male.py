#!/usr/bin/python

import math
from scipy.stats import norm, logistic, uniform

# a male individual in the population
class Male(object):
    # constructor
    def __init__(self, params, logger, id, mom = None, dad = None):
        self.id = id

        self.logger = logger

        # countdown timer to next event
        self.tt_event = 1.0
        
        self.metabolic_cost_search = params["metabolic_cost_search"]
        self.metabolic_cost_occupy = params["metabolic_cost_occupy"]

        self.occupying = False
        
        # pull the maturation time from the inverse logit
        self.maturation_time = abs(logistic.rvs(
            params["maturation_center"],
            params["maturation_width"]))

        #get mass at maturation:
        self.grow(params)

        # energy at maturation
        self.energy = self.mass * params["mass_to_energy"]

        # trait values
        if not mom and not dad: # first gen: no breeding
            self.exploration_trait = norm.rvs(params["exploration_mean"], params["exploration_sd"])

            # pull the aggression from the normal distribution
            self.aggro = params["aggression_max"] * uniform.rvs()

        elif not mom: # asexual genetics
            mutation_rate = params["mutation_rate"]
            mutation_sd = params["mutation_sd"]
            
            self.exploration_trait = dad.exploration_trait
            self.aggro = dad.aggro
            
            if uniform.rvs() < mutation_rate:
                self.exploration_trait += norm.rvs(0, mutation_sd)

            if uniform.rvs() < mutation_rate:
                self.aggro += norm.rvs(0, mutation_sd)

            if self.aggro < 0:
                self.aggro = 0

        self.exploration = logistic.cdf(
            self.exploration_trait / params["exploration_prob_scale"]
        )

            
    
    # mass from 0 to time t
    def grow(self, params):
        a = params["growth_param_a"]
        b = params["growth_param_b"]
        self.mass = pow(params["initial_mass"], 1.0 - b) 
        self.mass += self.maturation_time * a * ( 1.0 - b )
        self.mass = pow(self.mass, 1.0/(1.0 - b))
    
    # a male explores its surroundings
    # returns true if the male has discovered a nest
    # false if otherwise
    def search(self, dt):
        self.tt_event -= dt
        spent = dt * self.metabolic_cost_search
        self.energy -= spent
        self.logger.inc_search_energy(spent)

        if self.tt_event <= 0:
            self.tt_event = 1.0
            if uniform.rvs() < self.exploration:
                return True
        return False


    def is_alive(self):
        return self.energy >= 0

    def occupy(self, dt):
        spent = dt * self.metabolic_cost_occupy
        self.logger.inc_occupying_energy(spent)
        self.energy -= spent


    def to_string(self):
        return "%s: explor=%s\tmat=%s\tM=%s\tE=%s" % (
            self.id,
            self.exploration,
            self.maturation_time,
            self.mass,
            self.energy)