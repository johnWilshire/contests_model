library(jsonlite)

# I am guessing that you are in the top dir

setwd("python/data")
df <- lapply(
  dir(), 
  function (filename){ 
    cat(filename)
    fromJSON(filename)
  }
)
setwd("../..")





