library(httr)
library(jsonlite)

url <- "https://trial.dominodatalab.com/v1/Jim89/quick-start/endpoint"
dominoApiHeaders <- add_headers("X-Domino-Api-Key" = domino_key)
response <- POST(url, dominoApiHeaders, body=toJSON(list(parameters=c("Jim"))), content_type("application/json"))
ans <- (content(response))
ans$result
