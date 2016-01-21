# a class to hold data logs of generations:

import numpy as np
import sys
import matplotlib.pyplot as plt

# TODO make 1 logger per simulation which aggregates generation data
# TODO rename to generation logger
# TODO make energy time series used a %

class Logger(object):
    """docstring for logs"""
    def __init__(self, generation):
        self.generation = generation

        self.searching = 0
        self.killed = 0
        self.num_matured = 0
        self.occupying = 0
        self.contests = 0
        self.take_overs = 0
        
        # total energy expenditure
        self.search_energy = 0
        self.contest_energy = 0
        self.occupying_energy = 0

        self.data = []

    # this function should be called each time step
    # to log the generation to the data list
    def log_cohort(self):
        row = {}
        # average energy of searching males
        row["time"] = self.generation.time
        row["searching"] = self.searching
        row["occupying"] = self.occupying
        row["contests"] = self.contests 
        row["num_matured"] = self.num_matured
        row["killed"] = self.killed
        row["take_overs"] = self.take_overs

        row["search_energy"] = self.search_energy
        row["contest_energy"] = self.contest_energy
        row["occupying_energy"] = self.occupying_energy

        self.data.append(row)

    def get_col(self, col_name):
        return [ row[col_name] for row in self.data ]

    def plot_cohort(self):
        self.plot_time_series()
        self.plot_e_time_series()
        self.plot_trait_hist()
        self.plot_trait_scatter()

    def plot_time_series(self):
        times = self.get_col("time")
        searching = self.get_col("searching")
        occupying = self.get_col("occupying")
        contests = self.get_col("contests")
        num_matured = self.get_col("num_matured")
        killed = self.get_col("killed")
        take_overs = self.get_col("take_overs")

        plt.title("Gen %s Various generation metrics through time. dt = %s" 
                % ( self.generation.id, self.generation.params["time_step"]))
        plt.xlabel("time steps")

        plt.plot(times, searching, label = "searching males")
        plt.plot(times, occupying, label = "occupying males")
        plt.plot(times, contests, label = "total contests")
        plt.plot(times, num_matured, label = "total matured males")
        plt.plot(times, killed, label = "total deaths")
        plt.plot(times, take_overs, label = "take overs")

        plt.legend(loc = 2)
        plt.show()

    def plot_e_time_series(self, savefig = False):
        times = self.get_col("time")

        search_energy = self.get_col("search_energy")
        contest_energy = self.get_col("contest_energy")
        occupying_energy = self.get_col("occupying_energy")

        plt.title("Gen %s: total Energy expenditure through time. delta = %s" 
                % (self.generation.id, self.generation.params["time_step"]))
        plt.xlabel("Time")
        plt.ylabel("Energy expenditure (J)")
        plt.axis([times[0],times[-1],0,self.generation.params["energy_y_max"]])

        plt.stackplot(times,
            search_energy,
            occupying_energy,
            contest_energy)

        p1 = plt.Rectangle((0, 0), 1, 1, fc="red")
        p2 = plt.Rectangle((0, 0), 1, 1, fc="green")
        p3 = plt.Rectangle((0, 0), 1, 1, fc="blue")
        plt.legend([p1, p2, p3], ["search", "occupying", "contest"])
        if savefig:
            plt.savefig("plots/gen_%03d_total_energy_expenditure.png" % self.generation.id)
            plt.close()
            return
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
        plt.title("gen %s: trait distribution of winners" % self.generation.id)
        plt.show()

    def plot_trait_scatter(self, savefig = False):
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
        plt.plot(occupying_exploration_trait, occupying_aggro_trait, 'ro',)
        plt.title("gen %s: trait values of %s winners" %( self.generation.id, len(occupying_exploration_trait)))
        plt.axis([0,1,0,1])
        plt.xlabel("exploration prob")
        plt.ylabel("aggression trait")
        if savefig:
            plt.savefig("plots/gen_%03d_winner_trait_values.png" % self.generation.id)
            plt.close()
            return
        plt.show()

    def inc_occupying(self):
        self.occupying += 1

    def dec_occupying(self):
        self.occupying -= 1

    def inc_searching(self):
        self.searching += 1

    def dec_searching(self):
        self.searching -= 1

    def inc_contests(self):
        self.contests += 1

    def inc_num_matured(self):
        self.num_matured += 1

    def inc_killed(self):
        self.killed += 1
    
    def inc_take_overs(self):
        self.take_overs += 1

    def inc_search_energy(self, j):
        self.search_energy += j

    def inc_contest_energy(self, j):
        self.contest_energy += j
    
    def inc_occupying_energy(self, j):
        self.occupying_energy += j