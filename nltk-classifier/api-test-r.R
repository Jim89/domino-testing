library(httr)
library(jsonlite)

url <- "https://trial.dominodatalab.com/v1/Jim89/quick-start/endpoint"
dominoApiHeaders <- add_headers("X-Domino-Api-Key" = "Aa1eYnwdRinE9qwOy3xK1Si1xokifTLILBYVKDoHMEeS3EEGuRmX3rPK9qAVxh2z")
response <- POST(url, dominoApiHeaders, body=toJSON(list(parameters=c("Jim"))), content_type("application/json"))
ans <- (content(response))
ans$result
