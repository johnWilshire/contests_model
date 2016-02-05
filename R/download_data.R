# downloads the data from google docs
# not sure this is needed tbqh

get_data <- function(){
  library(httr)
  url <- "https://drive.google.com/uc?export=download&id=0B3rkdRF2R-5rbVNlQzRFU3ZwLVU"
  # I think there might be an issue with a prompt, also where to save the data?
  GET(url)
}