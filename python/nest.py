#!/usr/bin/python
import sys
from scipy.stats import logistic, uniform
from male import Male
""" a nest has a RR and female genetics and a male occupier"""

""" TODO
    abandoning nests
    check winner is alive after contest
"""
class Nest(object):

    def __init__(self, params, id):
        self.id = id
        self.rr = params["rr_mean"]
        self.fight_cost = params["fight_cost"]
        self.display_1_cost = params["display_1_cost"]
        self.occupier = None
        self.debug = params["debug"]

    def occupied(self):
        return bool(self.occupier)

    def contest(self, attacker):
        defender = self.occupier

        # energy costs associated with this contest
        costs = 0
        loser = None

        if not defender.is_alive():
            loser = defender

        if not loser:
            loser = self.display_1(attacker, defender)
            costs += self.display_1_cost

        # fight
        if not loser:
            loser = self.fight(attacker, defender)
            costs += self.fight_cost
        
        attacker.energy -= costs
        defender.energy -= costs

        attacker.logger.inc_contest_energy(costs)
        defender.logger.inc_contest_energy(costs)


        if loser.id == defender.id:
            self.eject()
            self.occupy(attacker)
        return loser

    # the first display phase, the loser is returned or None
    def display_1(self, attacker, defender):
        ## attacker goes first
        # prob the attacker will escalate
        if self.debug:
            print "fight!"
            print "attacker mass = %s, attacker aggro = %s" % (attacker.mass, attacker.aggro)
            print "defender mass = %s, defender aggro = %s" % (defender.mass, defender.aggro)
        
        atk_escalation = logistic.cdf(attacker.mass * attacker.aggro - defender.mass)
        rng = uniform.rvs()
        
        if rng > atk_escalation :
            # attacker decides to escalate
            if self.debug:
                print "%s > %s" % (rng, atk_escalation)
                print "\tattacker backs down"
            return attacker
        else:
            if self.debug:
                print "%s <= %s" % (rng, atk_escalation)
                print "\tattacker escalates"
        
        def_escalation = logistic.cdf(defender.mass * defender.aggro - attacker.mass)
        rng = uniform.rvs()
        if rng > def_escalation:
            if self.debug:
                print "%s > %s" % (rng, def_escalation)
                print "\tdefender backs down"
            return defender
        else:
            if self.debug:
                print "%s <= %s" % (rng, def_escalation)
                print "\tdefender escalates"

        return None

    def fight(self, attacker, defender):
        if self.debug:
            print "fight"
        defender_wins = logistic.cdf(defender.mass - attacker.mass)
        rng = uniform.rvs()
        if rng > defender_wins:
            if self.debug:
                print "%s > %s" % (rng, defender_wins)
                print "\tattacker wins"
            return defender
        else:
            if self.debug:
                print "%s <= %s" % (rng, defender_wins)
                print "\tdefender wins"
            return attacker


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
        return [Male(params, logger, i, dad = self.occupier) for i in range(id_start, id_start + self.rr) ]
