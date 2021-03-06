# a class to hold data logs of a generation:

import numpy as np
import sys
import matplotlib.pyplot as plt

class GenerationLogger(object):
    """docstring for logs"""
    def __init__(self, generation):
        self.generation = generation

        self.searching = 0
        self.killed = 0
        self.num_matured = 0
        self.occupying = 0
        self.contests = 0
        self.take_overs = 0 
        self.search_energy = 0
        self.contest_energy = 0
        self.occupying_energy = 0

        self.data = {
            "time":[0],
            "searching":[0],
            "killed":[0],
            "num_matured":[0],
            "occupying":[0],
            "contests":[0],
            "take_overs":[0],
            "search_energy":[0],
            "contest_energy":[0],
            "occupying_energy":[0]
        }

        # records information about the contests that happen in a generation
        self.contest_data = {
            "fight_cost":[],
            "def_start_energy":[],
            "atk_start_energy":[],
            "def_end_energy":[],
            "atk_end_energy":[],
            "def_commit":[],
            "atk_commit":[],
            "atk_mass":[],
            "def_mass":[],
            "prob_upset":[],
            "defence_winner":[],
            "atk_alpha":[],
            "atk_alpha":[],
            "atk_beta":[],
            "def_alpha":[],
            "def_beta":[]
        }

    # this function should be called each time an event is processed
    def log_cohort(self):
        self.data["time"].append(self.generation.time)
        self.data["searching"].append(self.searching)
        self.data["occupying"].append(self.occupying)
        self.data["contests"].append(self.contests) 
        self.data["num_matured"].append(self.num_matured)
        self.data["killed"].append(self.killed)
        self.data["take_overs"].append(self.take_overs)        
        self.data["search_energy"].append(self.search_energy)      
        self.data["contest_energy"].append(self.contest_energy)        
        self.data["occupying_energy"].append(self.occupying_energy)

    def log_contest(self, contest_info_dict):
        for key in contest_info_dict:
            self.contest_data[key].append(contest_info_dict[key])


    def get_col(self, col_name):
        return [ row[col_name] for row in self.data ]

    def plot_cohort(self):
        self.plot_time_series()
        self.plot_e_time_series()
        self.plot_trait_hist()
        self.plot_trait_scatter()

    def plot_time_series(self, savefig = False):
        times = self.data["time"]
        searching = self.data["searching"]
        occupying = self.data["occupying"]
        contests = self.data["contests"]
        num_matured = self.data["num_matured"]
        killed = self.data["killed"]
        take_overs = self.data["take_overs"]

        occupying_males = self.get_occupying_males()

        winners_matured = np.mean([m.maturation_time for m in occupying_males])
                
        plt.title("Gen %s Various generation metrics through time." 
                % ( self.generation.id))
        plt.xlabel("time steps")

        plt.plot(times, searching, label = "searching males")
        plt.plot(times, occupying, label = "occupying males")
        plt.plot(times, contests, label = "total contests")
        plt.plot(times, num_matured, label = "total matured males")
        plt.plot(times, killed, label = "total deaths")
        plt.plot(times, take_overs, label = "take overs")

        plt.axvline(winners_matured, color='k', linestyle='--')
        plt.text(winners_matured + 0.1,1400,'average winner matured',rotation=90)

        plt.legend(loc = 2)
        if savefig:
            plt.savefig("plots/gen_%03d_time_series.png" % self.generation.id)
            plt.close()
            return
        plt.show()

    def plot_e_time_series(self, savefig = False):
        times = self.data["time"]

        search_energy = self.data["search_energy"]
        contest_energy = self.data["contest_energy"]
        occupying_energy = self.data["occupying_energy"]

        plt.title("Gen %s: total Energy expenditure through time" 
                % (self.generation.id))
        plt.xlabel("Time")
        plt.ylabel("Energy expenditure (J)")

        plt.stackplot(times,
            search_energy,
            occupying_energy,
            contest_energy)

        # plot the legend
        p1 = plt.Rectangle((0, 0), 1, 1, fc="red")
        p2 = plt.Rectangle((0, 0), 1, 1, fc="green")
        p3 = plt.Rectangle((0, 0), 1, 1, fc="blue")
        plt.legend([p3, p2, p1], ["search", "occupying", "contest"])

        if savefig:
            plt.savefig("plots/gen_%03d_total_energy_expenditure.png" % self.generation.id)
            plt.close()
            return
        plt.show()

    def plot_trait_hist(self):
        occupying_males = self.get_occupying_males()
        if len(occupying_males) == 0:
            print "extintion event"

        winner_exploration_trait = [
            m.exploration
            for m in occupying_males
        ]
        winner_e_0_trait = [
            m.e_0
            for m in occupying_males
        ]
        winner_k_trait = [
            m.k
            for m in occupying_males
        ]

        plt.boxplot([winner_k_trait,winner_e_0_trait, winner_exploration_trait])
        labels = ('k aggression', 'e_0 aggression', 'exploration (2 * r * v)')
        plt.xticks([1,2,3],labels)
        plt.legend()
        plt.title("gen %s: trait distribution of winners" % self.generation.id)
        plt.show()

    """ plots the aggression traits """
    def plot_trait_scatter(self, savefig = False):
        winners = self.get_occupying_males()
        winners_e_0_traits = [
            m.e_0
            for m in winners
        ]
        winners_k_traits = [
            m.k
            for m in winners
        ]

        plt.plot(winners_k_traits, winners_e_0_traits, 'ro',)
        plt.title("gen %s: aggrssion trait values of %s winners" %( self.generation.id, len(winners_k_traits)))
        plt.axis([-20,20,-20,20])
        plt.xlabel("k trait")
        plt.ylabel("e_0 trait")
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

    def get_occupying_males(self):
        return [
            n.occupier 
            for n in self.generation.winners
        ]