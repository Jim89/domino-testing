# Domino Testing
Jim Leach  
7 January 2017  

## Overview

Testing out the Domino platform has been great. It works really nicely and I was able to easily create two simple examples of things I can imagine using a lot. End-to-end these two exercises probably took only 2 hours to put together, starting from scratch and with no experience using Domino before. 

I think this is a testament to both the platform itself (the functionality seems pretty intuitive) as well as the very helpful [documentation](http://support.dominodatalab.com/hc/en-us). 

As well as saving everything in a simple, public project on the Domino platform [here](https://trial.dominodatalab.com/u/Jim89/domino-testing/overview) I also created a small `GitHub` repository with my code in which lives [here](https://github.com/Jim89/domino-testing).

I had two exercises that I worked on. First, create a simple classifier with the Natural Language Tool Kit (`nltk`) in `Python` and deploy and API endpoint on the Domino platform to use that classifier for some simple text classification. Secondly, I created a Launcher on the platform that used let's a user upload a text file of numbers (one per line) and then uses `R` (and the `knitr` package) to create a simple `HTML` report with some simple summary statistics and a histogram.

## `nltk` Text classification API

Creating a simple API endpoint on Domino turned out to be very straightforward. I decided to use a simple [example](http://www.nltk.org/book/ch06.html) classifier from the `nltk` documentation: classifying names as male or female, based only on the last letter of the name [Bird, Klein and Loper, 2009]. 

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

I then followed the documentations intructions for publishing the function as an API endpoint. I:

1. Selected _Publish_ in the Domino menu
2. Clicked on to _API Endpoint_
3. Added the filename (`get-gender.py`) of my classifier in the 'file containing code to invoke' box
4. Added my classification function (`get_gender()`) to the 'function to invoke' box
5. Clicked publish

Everything seemed to have worked smoothly, so I tested out the functionality with the simple `Python` script provided. It seemed to be working as expected, so I tried `R` as well (typically the language I'd turn to first):


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

The API creation functionality was fantastic and very straightforward: from start to finish I was able to get it working in about 1 hour (and that included some time for me tinkering with `nltk` locally before getting things set up on Domino). Really impressive stuff and I'm keen to keep using this in the future.

## Basic stats launcher

1. Launchers -> New launcher
2. Create example launcher
3. Create first test launcher with basic script - works, but dones't generate output
4. Switch to Rmd file for script - works but doesn't accept parameters so can't pass it the file
5. Use script to read in data then run render to create HTML file which works because the data exists in the same environment (horrible hack but works for now)
6. Tidy up Rmd file to produce neat output in HTML

Total time: 45 minutes

Sources:

http://support.dominodatalab.com/hc/en-us/articles/204139569-Launchers#tutorial

***

## References

1. Bird, Klein and Loper, _Natural Language Processing with Python_, 2009, Chapter 6 - Learning to Classify Texts. [Link](http://www.nltk.org/book/ch06.html).
2. Domino Data Labs, _API Endpoints and Model Deployment_, [Link](http://support.dominodatalab.com/hc/en-us/articles/204173149-API-Endpoints-Model-Deployment)
3. Domino Data Labs, _Launchers_, [Link](http://support.dominodatalab.com/hc/en-us/articles/204139569-Launchers)