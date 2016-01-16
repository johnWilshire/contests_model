# a class to hold data logs of generations:

import numpy as np
import sys
import matplotlib.pyplot as plt

class Logger(object):
    """docstring for logs"""
    def __init__(self, generation):
        self.generation = generation
        self.data = []

    # this function should be called each time step
    # to log the generation to the data list
    def log_cohort(self):
        row = {}
        # average energy of searching males
        row["time"] = self.generation.time
        row["searching"] = len(self.generation.searching)
        row["occupying"] = self.generation.occupying
        row["contests"] = self.generation.contests 
        row["num_matured"] = self.generation.num_matured
        row["killed"] = self.generation.killed

        row["energy_searching"] = np.mean([m.energy for m in self.generation.searching])
        row["energy_occupying"] = np.mean([n.occupier.energy 
                                            for n in self.generation.nests
                                                if n.occupied()])
        self.data.append(row)

    def get_col(self, col_name):
        return [ row[col_name] for row in self.data ]

    def plot_cohort(self):
        self.plot_time_series()
        self.plot_E_time_series()
        self.plot_trait_hist()
        self.plot_trait_scatter()

    def plot_time_series(self):
        times = self.get_col("time")
        searching = self.get_col("searching")
        occupying = self.get_col("occupying")
        contests = self.get_col("contests")
        num_matured = self.get_col("num_matured")
        killed = self.get_col("killed")

        plt.title("Various generation metrics through time. dt = %s" 
                % self.generation.params["time_step"])
        plt.xlabel("time steps")

        plt.plot(times, searching, label = "searching males")
        plt.plot(times, occupying, label = "occupying males")
        plt.plot(times, contests, label = "total contests")
        plt.plot(times, num_matured, label = "total matured males")
        plt.plot(times, killed, label = "total deaths")

        plt.legend(loc = 2)
        plt.show()

    def plot_E_time_series(self):
        times = self.get_col("time")
        mean_energy_searching = self.get_col("energy_searching")
        mean_energy_occupying = self.get_col("energy_occupying")

        plt.title("Mean energy levels through time. delta = %s" 
                % self.generation.params["time_step"])
        plt.xlabel("time steps")
        plt.ylabel("mean Energy values (J)")
        plt.plot(times, mean_energy_searching, label = "searching")
        plt.plot(times, mean_energy_occupying, label = "occupying")
        plt.legend(loc = 1)
        plt.show()

    def plot_trait_hist(self):
        occupying_males = [
            n.occupier 
            for n in self.generation.nests 
            if n.occupied()
        ]
        if len(occupying_males) == 0:
            print "extintion event"

        occupying_exploration_trait = [
            m.exploration 
            for m in occupying_males
        ]
        occupying_aggro_trait = [
            m.aggro / self.generation.params["aggression_max"]
            for m in occupying_males
        ]

        bins = self.generation.params["trait_bins"]
        hist_range = (0,1)

        plt.hist(occupying_exploration_trait,
            range = hist_range,
            bins = bins,
            alpha = 0.3,
            label = "exploration")

        plt.hist(occupying_aggro_trait,
            range = hist_range,
            bins = bins,
            alpha = 0.3,
            label = "aggression")
        plt.legend()
        plt.title("%s: trait distribution of winners" % self.generation.id)
        plt.show()

    def plot_trait_scatter(self):
        occupying_males = [
            n.occupier 
            for n in self.generation.nests 
            if n.occupied()
        ]

        occupying_exploration_trait = [
            m.exploration
            for m in occupying_males
        ]
        occupying_aggro_trait = [
            m.aggro / self.generation.params["aggression_max"]
            for m in occupying_males
        ]
        plt.plot(occupying_exploration_trait, occupying_aggro_trait, 'ro')
        plt.title("trait values of winners")
        plt.xlabel("exploration trait")
        plt.ylabel("aggression trait")
        plt.show()