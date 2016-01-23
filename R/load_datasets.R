library(jsonlite)
library(ggplot2)

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

master <- data.frame()

# this works but feels pretty gross
 
# Will please teach me the R way


for (simulation in df){
    simulation <- data.frame(
      # select these columns for analysis
      simulation$traits.aggression,
      simulation$parameters.patch_area
    )
    # rename them
    colnames(simulation) <- c(
      "aggression",
      "patch_area"
    )
    master <- rbind(master, simulation)
}

setwd("../..")

ggplot(master,aes(x = patch_area, y = aggression, colour = aggression)) + geom_point() + scale_color_gradient(low="blue",high="red")
#ggplot(master,aes(x = patch_area, y = aggression)) + geom_density2d()

#qplot(y = master$aggression, x = master$patch_area )
.


