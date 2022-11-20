# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 18:19:21 2022

@author: Rohan
"""
from pagerank import *

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
# page = "1.html"
damping_factor = 0.85
# print(transition_model(corpus, page, damping_factor))

# weights = {"half": 0.5, "quarter": 0.25, "sixth": 1/6, "twelfth": 1/12}
# counts = {i: 0 for i in weights.keys()}
# for i in range(1000000):
#     cumulative = 0
#     seed = random.random()
#     for fraction, probability in weights.items():
#         cumulative += probability
#         if cumulative > seed:
#             counts[fraction] += 1
#             break
# proportions = {fraction: count / 1000000 for fraction, count in counts.items()}
# print(proportions)


# print(sample_pagerank(corpus, damping_factor, 10000))
print(iterate_pagerank(corpus, damping_factor))
