# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 21:27:45 2022

@author: Rohan
"""
from heredity import *

people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

print(joint_probability(people, {"Harry"}, {"James"}, {"James"}))