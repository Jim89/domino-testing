# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 11:05:36 2017

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
males = open("./male.txt", "r").read().split('\n')
females = open("./female.txt", "r").read().split('\n')

# Remove 0-length names (import errors)
males = filter(len, males)
females = filter(len, females)

# Now label the names
labelled_names = ([(name, 'male') for name in males] + [(name, 'female') for name in females])
   
# Then randomly shuffle them up
import random
random.shuffle(labelled_names)    

# Then pull out the simple feature (last letter) for each name, along with the specified gender
featuresets = [(gender_feature(n), gender) for (n, gender) in labelled_names]  

# Then split into test and train
train, test = featuresets[500:], featuresets[:500]  

# Create a dead-simple Naive-Bayes classifier from the train set
import nltk
classifier = nltk.NaiveBayesClassifier.train(train)

import joblib
joblib.dump(classifier, 'nltk-classifier.pkl')