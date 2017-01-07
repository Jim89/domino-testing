# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 11:43:41 2017

@author: jim
"""

import requests
 
response = requests.post("https://trial.dominodatalab.com/v1/Jim89/quick-start/endpoint",
    headers = {
        "X-Domino-Api-Key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json = {
        "parameters": ["Jim"]
    }
)
 
print(response.status_code)
print(response.headers)
print(response.json())

print('\n\nThe answer is:')
print(response.json()['result'])
