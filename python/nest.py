#!/usr/bin/python
import sys
from scipy.stats import logistic, uniform
from male import Male

""" TODO
    
    make sure that if the winner is dead at the end of the contest 
    and the loser is alive then the loser becomes the winner

"""
class Nest(object):
    """ a nest can have a male occupier or be empty"""

    def __init__(self, params, id):
        self.id = id
        self.params = params
        self.occupier = None

    def occupied(self):
        return bool(self.occupier)

    def contest(self, attacker):
        """ a contest between males, the winner gets to occupy the nest"""
        defender = self.occupier

        if not defender.is_alive():
            self.eject()
            self.occupy(attacker)
            return defender


        defender_commitment = defender.get_commitment(attacker)
        attacker_commitment = attacker.get_commitment(defender)

        # the defender wins
        if defender_commitment >= attacker_commitment:
            winner = defender
            loser = attacker
            delta_commitment = defender_commitment - attacker_commitment
            cost = self.energy_spent(attacker_commitment)
        else: # the attacker wins
            winner = attacker
            loser = defender
            delta_commitment = attacker_commitment - defender_commitment
            cost = self.energy_spent(defender_commitment)

        # the winner wins with probability equal to the difference in commitment
        # the chance of an upset happening is :
        if logistic.cdf(delta_commitment) > uniform.rvs():
            temp = winner
            winner = loser
            loser = temp

        # make sure no more than the max energy of either male can be deducted
        cost = min([winner.energy, loser.energy, cost])
        
        # the costs are deducted
        attacker.energy -= cost
        defender.energy -= cost
        if self.params["debug"]:
            print "\tfight cost =", cost
            print "winner = %s , loser = %s" % (winner.id, loser.id)

        # the costs logged
        attacker.logger.inc_contest_energy(cost)
        defender.logger.inc_contest_energy(cost)

        if not defender.is_alive():
            loser = defender

        if loser == defender:
            self.eject()
            self.occupy(attacker)

        return loser

    # the cost of a fight that has escalated from 0 to the commitment given
    def energy_spent(self, commitment):
        return ((commitment ** 3)/3.0) if commitment >= 0 else 0


    # remove and return the current  from the nest
    def eject(self): 
        m = self.occupier
        self.occupier = None
        return m


    # insert a given male into the nest
    def occupy(self, m):
        if self.occupier:
            sys.exit("eject old male before occpying")
        self.occupier = m

    # returns a list of male progeny from this nest
    def get_offspring(self, params, logger, id_start):
        return [
                Male(params, logger, i, dad = self.occupier) 
                for i in range(id_start, id_start + self.params["rr_mean"])
            ]
