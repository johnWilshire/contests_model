# Thoughts towards a paper about a dynamic contests model

To compile the paper we use [remake](https://github.com/traitecoevo/remake).  The easiest way to install remake is via [drat](https://github.com/eddelbuettel/drat):

```r
drat:::add("traitecoevo")
install.packages("remake")
```

(install drat itself with `install.packages("drat")`)

Compilation requires a reasonably complete LaTeX installation (e.g. MacTeX).

We use the non-CRAN packages [callr](https://github.com/traitecoevo/callr).  This can be installed by remake:

```r
remake::install_missing_packages()
```

To compile everything, run

```r
remake::make()
```

parameters can be modified by changing the values in ```parameters.jsons```

to run the simulation:
change to the python directory and run the command

```
python simulation.py
```
in your terminal

Explanation of parameters in ```parameters.json```

parameter           | explanation
----------          |-------------
random_seed         | the seed for the random number generator
debug               | if true detailed messages about what is happening ieach gen will be printed
generation_plot     | if true interactive plots will be shown at the end of each gen
    
save_pngs           | if true png's will be saved of the scatter plots
save_every          | which generations will be saved to png
initial_plot        | if true will display an interactive plot after the first gen
trait_bins          | the number of bins in the trait histogram          
final_plot          |if true will display an interactive plot after the final gens
generations         | how many generations to run the simulation for
-----------------   | ---------------------------
time_female_maturity| when do the females mature
time_step           | the delta time for each
N                   | the initial number of nests
K                   | the initial number of individuals
rr_mean             | the average reproductive power of a nest
rr_sd               | the standard deviation of reproductive power of a nest
maturation_center   | the point of inflection for the logistic male maturation function  
maturation_width    | the scale of the logistic male maturation function
growth_param_a      | see ms.pdf eqn 3,4
growth_param_b      | see ms.pdf eqn 3,4
initial_mass        | the mass of the males at time 0
mass_to_energy      | a male with m mass gets this m * this value starting energy
metabolic_cost_search | the cost of searching for nests per timestep
metabolic_cost_occupy | the cost of occupying a nest per time step
display_1_cost        | the cost of escalating to display 1
fight_cost            | the cost of escalating to a fight
aggression_max        | the maximum value for aggression allowed
exploration_mean      | the inital mean value for the distribution of exploration traits
exploration_sd        | the inital standard deviation for the distribution 
exploration_prob_scale| exploration = logistic.cdf (exploration trait / this)
mutation_rate         | chance that a trait will mutate
mutation_sd           | the standard deviation of a mutation, 0 mean