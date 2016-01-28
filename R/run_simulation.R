
library(parallel)

# this function runs the simulation
# it assumes that you are in the python directory
run_simulation <- function (to_modify, lower, upper, by){
  points <- seq(lower, upper, by = by)
  mclapply(points,
    function (point){
      system(paste("python simulation.py", to_modify, point)) 
    },
    mc.cores = 8
  )
}