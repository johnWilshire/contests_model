# loads the dataset of trait values and parameters
# returns a data.frame
load_population  <- function (){
  setwd("python/data")
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
  setwd("../..")
  return(master)
}

# loads the trait history
# and energy
# returns a data.frame

load_trait_history  <- function (){
  setwd("python/data")
  traits <- lapply(
    dir()[grep("*.json", dir())], 
    function (filename){ 
      as.data.frame(
        # ignore the trait history portion
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
  setwd("../..")
  return(master)
}