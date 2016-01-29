library(jsonlite)
library(ggplot2)
load_dataset  <- function (){
  df <- lapply(
    dir()[grep("*.json", dir())], 
    function (filename){ 
      as.data.frame(
        fromJSON(filename)
      )
    }
  )
  
  # this doesnt feel like the right way to do this
  # I cant do a plyr join as they might not have the same number of columns as I modify
  master <- data.frame()
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
  return(master)
}

make_plot <- function (master){
  print(ggplot(master, aes(x = patch_area, y = aggression)) + geom_density2d())
  
  print(ggplot(master, aes(x = patch_area, y = aggression, colour = aggression)) + geom_point() + scale_color_gradient(low="blue",high="red"))
  
  print(qplot(df$aggression, fill = as.factor(df$patch_area)))
}


