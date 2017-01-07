# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 10:39:29 2017

@author: jim
"""

#==============================================================================
# Create simple classifier for gender based purely on name
# Example as shown in http://www.nltk.org/book/ch06.html
#==============================================================================

# First up, define a simple feature extractor based on the last letter of the name
# (shown to be gender-informative)
def gender_feature(word):
    return {'last_letter': word[-1]}
    
# Now pull through the sample of names from nltk to prepare list of example names
from nltk.corpus import names 

# Now label the names
labelled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
   
# Then randomly shuffle them up
import random
random.shuffle(labelled_names)    

# Then pull out the simple feature (last letter) for each name, along with the specified gender
featuresets = [(gender_feature(n), gender) for (n, gender) in labelled_names]  

# Then split into test and train
train, test = featuresets[500:], featuresets[:500]  

# Create a dead-simple Naive-Bayes classifier from the train set
classifier = nltk.NaiveBayesClassifier.train(train)

# Do a couple of test examples
classifier.classify(gender_feature('Jim'))
classifier.classify(gender_feature('Max'))
classifier.classify(gender_feature('Joy'))
classifier.classify(gender_feature('Ogale'))

# Get overall in-sample accuracy
nltk.classify.accuracy(classifier, train)

# And out-of-sample:
nltk.classify.accuracy(classifier, test)

# Right, I know this is likely to be a crap classifier, but I need to get it working in Domino, so let's look at that now!

# Need to add a function that will return the gender given a name!
def get_gender(name):
    last_letter = gender_feature(name)
    gender = classifier.classify(last_letter)
    return gender