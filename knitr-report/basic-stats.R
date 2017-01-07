# Get the arguments from the launcher
args <- commandArgs(trailingOnly = TRUE)

# Extract the file
file <- args[1]

# Read in the file
data <- read.csv(file, header = F)

# Throw error if more than one column, else throw error
stopifnot(ncol(data) == 1)

# Set column names
names(data) <- "x"

rmarkdown::render("./basic-stats.Rmd")

