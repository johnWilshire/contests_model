#!/usr/bin/python

""" a nest has a RR and female genetics and a male occupier"""
class Nest(object):

    def __init__(self, params):
        self.rr = 0
        self.female = []
        self.male = []
        self.occupied = False