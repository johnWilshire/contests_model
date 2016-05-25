# loads the dataset of trait values and parameters across all generations
# returns a data.frame
# args:
# directory: the folder in which the collection of jsons will be read from

load_population  <- function (directory  = ""){
  master <- ldply(Filter(function (x) grepl("json", x), 
                         list.files(directory, full.names = TRUE)),                   
                  function (filename) {
                    as.data.frame(
                      fromJSON(filename, flatten = T)[c("traits", "parameters")]
                    )})
  colnames(master) <- sub("^[^.]*.","", colnames(master))
  return(master)
}

# loads the dataset of trait values and parameters across the latest generations
# returns a data.frame
# args:
# directory: the folder in which the collection of jsons will be read from
load_final_population  <- function (directory  = ""){
  master <- ldply(Filter(function (x) grepl("json", x), 
                         list.files(directory, full.names = TRUE)),                   
                  function (filename) {
                     m <- as.data.frame(fromJSON(filename)[c("traits", "parameters")])
                     filter(m, m$generation == max(m$generation))
                    })
  colnames(master) <- sub("^[^.]*.","", colnames(master))
  return(master)
}


# loads the trait history
# and energy
# returns a data.frame
load_trait_history  <- function (directory  = ""){
  master <- ldply(Filter(function (x) grepl("json", x), 
                         list.files(directory, full.names = TRUE)),                   
                  function (filename) {
                    as.data.frame(
                      fromJSON(filename, flatten = T)[c("history", "parameters")]
                    )})
  colnames(master) <- sub("^[^.]*.","", colnames(master))
  return(master)
}

load_contests  <- function (directory = ""){
  master <- ldply(Filter(function (x) grepl("json", x), 
                         list.files(directory, full.names = TRUE)),                   
                  function (filename) {
                    as.data.frame(
                      fromJSON(filename)[c("contests", "parameters")]
  )})
  colnames(master) <- sub("^[^.]*.","", colnames(master))
  return(master)
}

