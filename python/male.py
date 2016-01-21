#!/usr/bin/python

import math
from scipy.stats import norm, logistic, uniform

# a male individual in the population
class Male(object):
    # constructor
    def __init__(self, params, logger, id, mom = None, dad = None):
        self.id = id

        self.logger = logger

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
            self.radius = abs(norm.rvs(params["radius_mean"], params["radius_sd"]))
            self.speed = abs(norm.rvs(params["speed_mean"], params["speed_sd"]))
            # pull the aggression from the normal distribution
            self.aggro = params["aggression_max"] * uniform.rvs()

        elif not mom: # genetic inheritance from the dads
            mutation_rate = params["mutation_rate"]
            mutation_sd = params["mutation_sd"]
            
            self.radius = dad.radius
            self.speed = dad.speed
            self.aggro = dad.aggro
            
            if uniform.rvs() < mutation_rate:
                self.radius += norm.rvs(0, mutation_sd)

            if uniform.rvs() < mutation_rate:
                self.speed += norm.rvs(0, mutation_sd)

            if uniform.rvs() < mutation_rate:
                self.aggro += norm.rvs(0, mutation_sd)

            self.aggro = 0 if self.aggro < 0 else self.aggro
            self.speed = 0 if self.speed < 0 else self.speed
            self.radius = 0 if self.radius < 0 else self.radius

            if self.aggro < 0:
                self.aggro = 0

        self.exploration = 2 * self.radius * self.speed
        self.exploration_prob = (params["N"] * self.exploration * params["time_step"]) / params["patch_area"]

        self.metabolic_cost_search = params["search_energy_coef"] * self.radius * self.speed
        self.metabolic_cost_occupy = params["metabolic_cost_occupy"]
            
    
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
        spent = dt * self.metabolic_cost_search
        self.energy -= spent
        self.logger.inc_search_energy(spent)

        if uniform.rvs() < self.exploration_prob:
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

