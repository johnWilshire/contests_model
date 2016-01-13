#!/usr/bin/python
import sys

""" a nest has a RR and female genetics and a male occupier"""
class Nest(object):

    def __init__(self, params, id):
        self.id = id
        self.rr = 0
        self.occupier = None

    def occupied(self):
        return bool(self.occupier)

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
