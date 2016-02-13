# this script is called from the pbs script
args <- commandArgs(trailingOnly = TRUE)
source("../R/run_simulation.R")
run_simulation(args[1], 
    as.numeric(args[2]), 
    as.numeric(args[3]), 
    as.numeric(args[4]), 
    as.numeric(args[5]))