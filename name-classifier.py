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
    
# Now pull through the sample of names from nltk
    
    
