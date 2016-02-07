# loads the dataset of trait values and parameters
# returns a data.frame
# args:
# directory: the folder in which the collection of jsons will be read from
# levels: the number of levels to change directory back to
# ie python/data -> 2
load_population  <- function (directory  = "", levels = 0){
  setwd(directory)
  df <- lapply(
    dir()[grep("*.json", dir())], 
    function (filename){ 
      as.data.frame(
        # ignore the trait history portion
        fromJSON(filename)[1:2]
      )
    }
  )
  
  # this doesnt feel like the right way to do this
  # I cant do a plyr join as they might not have the same number of columns as I modify
  master <- data.frame()
  for (simulation in df){
    simulation <- data.frame(simulation)
    # rename them
    colnames(simulation) <- lapply(colnames(simulation), 
                                  function(x) {sub("^[^.]*.","",  x)})
    master <- rbind(master, simulation)
  }
  setwd(Reduce(function(...) {paste(..., sep = "")}, rep("../", levels)))
  return(master)
}

# loads the trait history
# and energy
# returns a data.frame

load_trait_history  <- function (directory  = "", levels = 0){
  setwd(directory)
  traits <- lapply(
    dir()[grep("*.json", dir())], 
    function (filename){ 
      as.data.frame(
        # read the trait history portion
        fromJSON(filename)[2:3]
      )
    }
  )
  master <- data.frame()
  for (simulation in traits){
    simulation <- data.frame(simulation)
    # rename them
    colnames(simulation) <- lapply(colnames(simulation), 
                                   function(x) {sub("^[^.]*.","",  x)})
    master <- rbind(master, simulation)
  }
  setwd(Reduce(function(...) {paste(..., sep = "")}, rep("../", levels)))
  return(master)
}