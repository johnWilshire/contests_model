#!/usr/bin/python

import math
from scipy.stats import norm, logistic, uniform, expon

# a male individual in the population
class Male(object):
    # constructor
    def __init__(self, params, logger, id, dad = None):
        self.id = id
        self.params = params
        self.events = []
        self.logger = logger

        # trait values
        if not dad: # first gen: no breeding
            self.radius = abs(norm.rvs(params["radius_mean"], params["radius_sd"]))
            self.speed = abs(norm.rvs(params["speed_mean"], params["speed_sd"]))
            # pull the aggression from the normal distribution
            self.k = abs(norm.rvs(params["k_mean"], params["k_sd"]))
            self.e_0 = abs(norm.rvs(params["e_0_mean"], params["e_0_sd"]))
            
            self.maturation_time = abs(logistic.rvs(
                params["maturation_center"],
                params["maturation_width"]))
        else: # genetic inheritance from the dads
            mutation_rate = params["mutation_rate"]
            mutation_sd = params["mutation_sd"]
            
            self.radius = dad.radius
            self.speed = dad.speed
            self.k = dad.k
            self.e_0 = dad.e_0

            if params["inherit_maturation_time"]:
                self.maturation_time = dad.maturation_time
                self.maturation_time += norm.rvs(0, params["maturation_noise"])
            else:
                self.maturation_time = abs(logistic.rvs(
                    params["maturation_center"],
                    params["maturation_width"]))

            # mutations
            if uniform.rvs() < mutation_rate:
                self.radius += norm.rvs(0, mutation_sd)

            if uniform.rvs() < mutation_rate:
                self.speed += norm.rvs(0, mutation_sd)

            if uniform.rvs() < mutation_rate:
                self.e_0 += norm.rvs(0, mutation_sd)

            if uniform.rvs() < mutation_rate:
                self.k += norm.rvs(0, mutation_sd)

            self.speed = 0 if self.speed < 0 else self.speed
            self.radius = 0 if self.radius < 0 else self.radius
            self.maturation_time = 0 if self.maturation_time < 0 else self.maturation_time

        #get mass at maturation:
        self.grow(params)

        # energy at maturation
        self.energy = self.mass * params["mass_to_energy"]
        self.energy_max = self.energy
        # see if this male lives to maturity
        self.time_last_event = self.maturation_time

        self.exploration = 2 * self.radius * self.speed
        self.exploration_rate = (params["N"] * self.exploration) / params["patch_area"]

        self.metabolic_cost_search = params["search_energy_coef"] * self.radius * self.speed
        self.metabolic_cost_occupy = params["search_energy_coef"] * self.radius * self.speed
        self.immature_mortality()
            
    
    # mass from 0 to time t
    def grow(self, params):
        a = params["growth_param_a"]
        b = params["growth_param_b"]
        self.mass = pow(params["initial_mass"], 1.0 - b) 
        self.mass += self.maturation_time * a * ( 1.0 - b )
        self.mass = pow(self.mass, 1.0 / (1.0 - b))
    
    # a male explores its surroundings
    # consumes energy from the time of the last event to now
    # removes the event from the list of events
    def search(self, event_time, final = False):
        spent = (event_time - self.time_last_event ) * self.metabolic_cost_search

        # if the male has died searching
        if spent >= self.energy:
            self.logger.inc_search_energy(self.energy)
            self.energy -= (spent + 1)
        else:
            self.time_last_event = event_time
            self.energy -= spent
            self.logger.inc_search_energy(spent)
        
        if not final:
            self.events.pop(0)

    # generates a random number to see if the male survived to maturity
    # based off maturation time
    # also some obvious catches
    def immature_mortality(self):
        survival = math.exp( -1.0 * self.params["immature_mortality_coef"] * self.maturation_time)
        if uniform.rvs() > survival:
            self.energy = -1
        if self.maturation_time > self.params["time_female_maturity"]:
            self.energy = -1
        if self.exploration <= 0:
            self.energy = -1

    def is_alive(self):
        return self.energy >= 0

    """ deducts the energy cost of occupying from the male"""
    def occupy(self, time):
        spent = (time - self.time_last_event) * self.metabolic_cost_occupy
        self.time_last_event = time
        self.logger.inc_occupying_energy(spent)
        self.energy -= spent

    # populates a list of discovery events for this male
    # from the given time to the end 
    def fill_events(self, time = -1):
        time = self.maturation_time if time == -1 else time
        
        self.events = []
        
        # pull the wait time from the exponential distrobution with rate parameter = exporation rate
        # in scipy.stats the rate parameter is scale = 1 / rate
        next_event = time + expon.rvs(scale = 1.0 / self.exploration_rate)
        
        while next_event < self.params["time_female_maturity"]:
            self.events.append(next_event)
            next_event += expon.rvs(scale = 1.0 / self.exploration_rate)

        # for if the first event is after the females mature
        self.events.append(1000000)


    # the commitment value for the male 
    def get_commitment(self, opponent):
        n_mass_difference = (self.mass - opponent.mass)/(self.mass + opponent.mass)
        return self.e_0 + (n_mass_difference * self.k)

    def to_string(self):
        return "%s: explor=%s\tmat=%s\tM=%s\tE=%s\t" % (
            self.id,
            self.exploration,
            self.maturation_time,
            self.mass,
            self.energy)

