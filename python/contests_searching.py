import scipy.stats as stats
import matplotlib.pyplot as plt
import math
import random

def main():
    data = dict()
    header = "time, matured"
    
    N = 100.0
    K = 100.0
    time_step = 100

    center = 50
    scale = 10
    lambda_ = 0.1
    
    newly_mature = 0.0
    searching = 0.0
    occupied = 0.0
    
    data["times"] = range(time_step + 1)
    data["matured"] = [0.0]
    data["searching"] = [0.0]
    data["occupied"] = [0.0]

    for t in data["times"][:-1]:
        data["matured"].append(K * stats.logistic.cdf(t, loc = center, scale = scale))
        newly_mature += data["matured"][-1] - data["matured"][-2]
        
        # as new males become mature they start to search
        while newly_mature > 1.0:
            newly_mature -= 1
            searching += 1

        # searching males finding nests
        m = searching
        while m > 0:
            # each searching male encounters a nest with probability lambda
            if lambda_ > random.random():
                # if the nest we encounter is unoccupied
                if random.random() > (occupied / N):
                    occupied += 1
                    searching -= 1
            m -= 1

        data["searching"].append(searching)
        data["occupied"].append(occupied)


    # data["occupying_percent"] = [100 * (data["occupied"][i] / data["matured"][i]) for i in range(1, time_step + 1)]
    # data["occupying_percent"] = [0] + data["occupying_percent"]

    plt.plot(data["times"], data["matured"], label = "matured")
    plt.plot(data["times"], data["searching"], label = "searching")
    plt.plot(data["times"], data["occupied"], label = "occupying")

    # plt.plot(data["times"], data["occupying_percent"], label = "occupying_percentage")
    plt.legend(loc = 2)
    plt.title("individuals, no contests once nest is occupied, lambda = %s" % (lambda_))
    plt.xlabel("time steps")
    plt.show()

if __name__ == '__main__':
    main()