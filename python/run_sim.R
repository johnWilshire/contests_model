# this script is called from the pbs script
args <- commandArgs(trailingOnly = TRUE)
args[2:5] <- as.numeric(args[2:5])

source("../R/run_simulation.R")
run_simulation(args[1], args[2], args[3], args[4], args[5])