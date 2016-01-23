library(jsonlite)
library(plyr)

# I am guessing that you are in the top dir

setwd("python/data")
df <- lapply(
  dir(), 
  function (filename){ 
    as.data.frame(
      fromJSON(filename)
    )
  }
)

# select these columns for analysis
master <- data.frame()

# this works but feels pretty gross and not R like
# will please teach me the R way

for (simulation in df){
    simulation <- data.frame(
      simulation$traits.aggression,
      simulation$parameters.patch_area
    )
    colnames(simulation) <- c(
      "aggression",
      "patch_area"
    )
    master <- rbind(master, simulation)
}

setwd("../..")



