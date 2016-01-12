from male import Male
from nest import Nest
# a generation in the minimal model
# aggregates males
# aggregates nests
# steps them through 1 generation of the simulation
class Generation:

    def run(self):
        # print the cohort
        for x in self.immature:
            print x.to_string() 
        
        # start the generation when the first males mature:
        time = self.immature[0].maturation_time
        print "start time\t", time


        # searching
        # occupying

        # iterate through time steps

        # for each male increment exploration by their lambda
        # when exploration reaches some value
        # pick a nest and occupy or contest



    # constructor for the first generation
    def __init__(self, params, prev_gen=None):
        self.params = params

        if not prev_gen:
            self.immature = list()
            self.searching = list()
            self.unoccupied_nests = list()
            self.occupied_nests = list()

            # create males
            self.immature = [Male(params) for _ in range(params["K"])]

            # sort males by when they mature
            self.immature.sort(key = lambda x : x.maturation_time)

            # pull from a range of RR's for nests
            self.unoccupied_nests = [Nest(params) for _ in range(params["N"])]
        else:
            # TODO
            # some genetics stuff here xD
            pass

        self.run()