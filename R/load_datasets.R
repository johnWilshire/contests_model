# loads the dataset of trait values and parameters
# returns a data.frame
# args:
# directory: the folder in which the collection of jsons will be read from
# plyr <3 <3 <3 <3 <3

load_population  <- function (directory  = ""){
  master <- ldply(list.files(directory, full.names = TRUE),                   
                  function (filename) {
                    data.frame(
                      fromJSON(filename)[1:2]
                    )})
  colnames(master) <- sub("^[^.]*.","", colnames(master))
  return(master)
}

# loads the trait history
# and energy
# returns a data.frame
# plyr <3 <3 <3
load_trait_history  <- function (directory  = ""){
  master <- ldply(list.files(directory, full.names = TRUE),                   
                  function (filename) {
                    data.frame(
                      fromJSON(filename)[2:3]
                    )})
  colnames(master) <- sub("^[^.]*.","", colnames(master))
  return(master)
}