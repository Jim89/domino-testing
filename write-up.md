# Domino Testing
Jim Leach  
7 January 2017  

## Overview

I had two exercises to work on: 

* First, create a simple classifier with the Natural Language Tool Kit (`nltk`) in `Python` and deploy and API endpoint on the Domino platform to use that classifier for some simple text classification. 
* Secondly, create a Launcher on the platform that used let's a user upload a text file of numbers (one per line). The launcher uses `R` (and the `knitr` package) to create a simple `HTML` report with some summary statistics and a histogram of the numbers.

Testing out the Domino platform has been great. It works really nicely and I was able to easily create two simple examples of things I can imagine using a lot. End-to-end these two exercises probably took only 2.5 hours to put together, starting from scratch and with no experience using Domino before. Writing this summary brings the total to about 3.5 hours. 

A great product with fantastic functionality, and straightforward to use, too. I think my ease-of-use experiences are a testament to both the platform (the functionality seems pretty intuitive) as well as the very helpful [documentation](http://support.dominodatalab.com/hc/en-us). 

As well as saving everything in a simple, public project on the Domino platform [here](https://trial.dominodatalab.com/u/Jim89/domino-testing/overview) I also created a small `GitHub` repository with my code in which lives [here](https://github.com/Jim89/domino-testing).

## `nltk` Text classification API

Creating a simple API endpoint on Domino turned out to be very straightforward. I decided to use a simple [example](http://www.nltk.org/book/ch06.html) classifier from the `nltk` book [Bird, Klein and Loper, 2009]: classifying names as male or female, based only on the last letter of the name. 

### Creating the classifier

The code for this example was really simple. First, I defined a simple function to extract the last letter from a name.


```python
def gender_feature(word):
    return {'last_letter': word[-1]}
```

Then, read in the sample names that come as part of the `nltk` package. Usually this is possible directly with `nltk`, but I ran in to some trouble with the Domino platform not having the necessary data files from `nltk`, so I loaded the two files manually.


```python
males = open("./male.txt", "r").read().split('\n')
females = open("./female.txt", "r").read().split('\n')

# Remove 0-length names (import errors)
males = filter(len, males)
females = filter(len, females)
```

Then I created a single data set with all the names, labelled them as either male or female and shuffled that list up to mix the two genders in together.


```python
labelled_names = ([(name, 'male') for name in males] + [(name, 'female') for name in females])

import random
random.shuffle(labelled_names) 
```

The `gender_feature` function was then used to extract the last letter from each name, retaining the label for the classifier. After splitting the data into train and test sets the classifier (a simple [Naive-Bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) model) was trained with the training data.


```python
featuresets = [(gender_feature(n), gender) for (n, gender) in labelled_names]  

# Then split into test and train
train, test = featuresets[500:], featuresets[:500]  

# Create a dead-simple Naive-Bayes classifier from the train set
import nltk
classifier = nltk.NaiveBayesClassifier.train(train)
```

I tested the accuracy on the testing set, just to get an idea of how well it would work. (It wasn't too important to have an accurate classifier for this exercise, but I was curious).


```python
nltk.classify.accuracy(classifier, test)
```

The model performed reasonably well, getting an accuracy on the test set of 76%. Not bad considering the feature used (just the last letter of the name)!

### Setting up the API endpoint.

Following the [documentation](http://support.dominodatalab.com/hc/en-us/articles/204173149-API-Endpoints-Model-Deployment) on the Domino page also proved very straightforward. The first thing I needed was a function that would accept an input (here, a new name) and then use the classifier to predict the gender:


```python
def get_gender(name):
    last_letter = gender_feature(name)
    gender = classifier.classify(last_letter)
    return gender
```

I added this to the end of my script as per the instructions, and uploaded the whole thing to the Domino platform [here](https://trial.dominodatalab.com/u/Jim89/domino-testing/view/get-gender.py). Initially I tried to create and save the model as a `pickle` in a separate script. (The documentation suggests that can be sensible for large models that take a while to train). However I ran into some trouble with the platform not having the right packages for this, so I kept all my code in one file. This felt reasonable given the simplicity of the model and the consequently very low training times. After this, I ran the code to make sure it worked with no errors on the Domino platform (it did).

I then followed the documentations instructions for publishing the function as an API endpoint. I:

1. Selected _Publish_ in the Domino menu
2. Clicked on to _API Endpoint_
3. Added the file name (`get-gender.py`) of my classifier in the 'file containing code to invoke' box
4. Added my classification function (`get_gender()`) to the 'function to invoke' box
5. Clicked publish

Everything seemed to have worked smoothly, so I tested out the functionality with the simple `Python` script provided:


```python
import requests
 
response = requests.post("https://trial.dominodatalab.com/v1/Jim89/quick-start/endpoint",
    headers = {
        "X-Domino-Api-Key": "MY_API_KEY",
        "Content-Type": "application/json"
    },
    json = {
        "parameters": ["Jim"]
    }
)

print('The answer is:')
print(response.json()['result'])
```

It seemed to be working as expected, so I tried accessing it from `R` as well (typically the language I'd turn to first):


```r
# Load the libraries we need
library(httr)
library(jsonlite)

url <- "https://trial.dominodatalab.com/v1/Jim89/domino-testing/endpoint"
dominoApiHeaders <- add_headers("X-Domino-Api-Key" = domino_key)
response <- POST(url, 
                 dominoApiHeaders, 
                 body = toJSON(list(parameters = c("Jim"))), 
                 content_type("application/json"))
ans <- (content(response))
ans$result
```

```
## [1] "male"
```

Again, working as expected. Just to see how the API handled multiple requests, I created a simple `R`function to test out the endpoint on a small handful of names.


```r
# Define function
get_gender_from_api <- function(name) {
  url <- "https://trial.dominodatalab.com/v1/Jim89/domino-testing/endpoint"
  dominoApiHeaders <- add_headers("X-Domino-Api-Key" = domino_key)
  response <- POST(url, 
                   dominoApiHeaders, 
                   body = toJSON(list(parameters = c(name))), 
                   content_type("application/json"))
  ans <- (content(response))
ans$result
}

sapply(c("Jim", "Max", "Joy", "Jake", "Martina"), get_gender_from_api)
```

```
##      Jim      Max      Joy     Jake  Martina 
##   "male" "female" "female" "female" "female"
```

The answers weren't 100% correct, but the endpoint was working as I expected it to, even with multiple requests. 

### Thoughts

The API creation functionality was fantastic and very straightforward: from start to finish I was able to get it working in about 1.5 hours (and that included time for me tinkering with `nltk` data files locally before getting things set up on Domino). Really impressive stuff and I'm keen to keep using this in the future.

## Basic stats launcher

Creating a launcher also turned out to be straightforward. I followed the basic [example](http://support.dominodatalab.com/hc/en-us/articles/204139569-Launchers#tutorial) from the Domino documentation and got that working to get a better understanding of how launchers work.

### Creating a script to run in the launcher

The basic premise of a launcher seemed to be: 

1. Create a script that can be run on demand, with or without extra parameters that can be specified by the user.
2. Set up a launcher to use that script.
3. Add the option for the user to specify parameters to the launcher.
4. Edit the script to use the parameters, maybe add more parameters, keep tinkering until you're happy with the results.

I was able to create a simple launcher with one parameter: a file type parameter to allow the user to upload a file. 

I created a simple `R` script that used this parameter and read in the list of numbers provided in the file by the user. I made sure that the launcher would throw an error if the uploaded file had more than one column, as I wanted the functionality to be really simple.


```r
# Get the arguments from the launcher
args <- commandArgs(trailingOnly = TRUE)

# Get just the file (the first parameter)
file <- args[1]

# Read in the file
data <- read.csv(file, header = F)

# Throw error if more than one column
stopifnot(ncol(data) == 1)

# Set column names
names(data) <- "x"
```

### Generating a HTML report

I initially tried to put this code into an `Rmd` file and use `knitr` directly in the launcher. However I couldn't see how to do that either in the launcher dialogue, or in the Domino documentation, so I instead created a very basic `Rmd` file separately that had the text and code I wanted to use to create the `HTML` report.

I then added a command to for `knitr` to process this file to the end of my existing script. The actual command comes from the `rmarkdown` package, but this calls `knit` underneath to create the output from the code. This works because the when the `Rmd` looks for the data supplied by the user, it finds it easily because the code above has read it in to `R` already. (Which is how I got around not being able to figure out if/how to add an `Rmd` script to the launcher directly).


```r
rmarkdown::render("./basic-stats.Rmd")
```

The `Rmd` file was very simple, containing some brief explanatory text, and the following code snippets to create the histogram, and a basic statistical summary of the numbers provided by the user:


```r
# Load packages
library(dplyr)
library(ggplot2)

# Create the histogram
ggplot(data, aes(x)) +
  geom_histogram(fill = "steelblue", colour = "white", bins = 30) +
  theme_minimal()

# Create the summary - use dplyr rather than summary() for easy tidying into a neat
# HTML table with knitr::kable()
data %>%
  summarise(min = min(x),
            first = quantile(x, 0.25),
            med = median(x),
            mean = mean(x),
            sd = sd(x),
            third = quantile(x, .75),
            max = max(x)) %>% 
  knitr::kable(col.names = c("Min", "1st Qu.", "Median", "Mean", "Std. Dev.", "3rd Qu.", "Max"))
```

I then tested the launcher and neatened up the HTML output slightly with a nicer theme. It seemed to be working as I was expected, which again was really nice.

### Thoughts 

In total I probably spent about 45 minutes tinkering with the launcher to get things working as I wanted them to be. Again I was impressed with Domino's functionality and the ease with which something like this simple report can be created. (Also) again, I'm keen to see more and I'll be testing Domino out further.

***

## References

1. Bird, Klein and Loper, _Natural Language Processing with Python_, 2009, Chapter 6 - Learning to Classify Texts. [Link](http://www.nltk.org/book/ch06.html).
2. Domino Data Labs, _API Endpoints and Model Deployment_, [Link](http://support.dominodatalab.com/hc/en-us/articles/204173149-API-Endpoints-Model-Deployment)
3. Domino Data Labs, _Launchers_, [Link](http://support.dominodatalab.com/hc/en-us/articles/204139569-Launchers)
