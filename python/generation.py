
# a generation in the minimal model
# aggregates males
# aggregates nests
# steps them through 1 generation of the simulation
class Generation:

    def run(self):
        # maturation


        # searching
        # occupying

        # iterate through time steps

        # for each male increment exploration by their lambda
        # when exploration reaches some value
        # pick a nest and occupy or contest



    # constructor for the first generation
    def __init__(self, params, prev_gen=None):
        self.N = params["N"]
        self.K = params["K"]

        if not prev_gen:
            self.immature = list()
            self.searching = list()
            self.nests = list()

            # create males
            for _ in range(K):
                self.immature.append(Male(params))

            # pull from a range of RR's for nests
            for _ in range(N):
                self.nests.append(Nest(params))
        else:
            # TODO
            # some genetics stuff here xD


        run()